import os
import re
import csv
import argparse
from Bio import SeqIO

## The following will parse the first argument given in the command line. Writing
## alpha.py C:/Documents/Test.txt will store the filepath as the variable file as an attribute of args.


parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('genus')
parser.add_argument('folderOutput')
args = parser.parse_args()


## using the file name provided at the command line the file is parsed for the necessary data in order to do the comparison. Newline characters and extra trailing and leading space will be removed from each line.

with open(args.file) as file:
	rawData = [item.strip() for item in file.readlines()]

## This class will represent an organism. It provides a constructor that will take the organismName as a string(HM27 for example), genomeFTP location as a string and transcriptomeFTP location as a string.
## This object has three attributes: Name, genomeFTP, and transcriptomeFTP. These will be used downstream in the pipeline for simplicity objects are used.

class Organism:
	def __init__(self, organismName, genomeFTPLocation, transcriptomeFTPLocation, featureFTPLocation):
		self.name = organismName
		self.genomeFTP = genomeFTPLocation
		self.transcriptomeFTP = transcriptomeFTPLocation
		self.featureFTP = featureFTPLocation

## Create a list of organism objects that's initally empty. THis is populated with objects based on what's in the file
## Each organsim object will contain the name of the organism, the ftp location of the genome, and the ftp location of the transcriptome.

listOfOrganisms = []
for organism in rawData:
	attributeList = organism.split(" ")
	organismObj = Organism(attributeList[0], attributeList[1], attributeList[2], attributeList[3])
	listOfOrganisms.append(organismObj)

	
## Makes a directory in the current working directory and switches into it as the current working directory for all of the following code.

os.system("mkdir " + args.folderOutput)
os.chdir(args.folderOutput)


## For every organism in the file it will get all of the data necessary for the pipeline to work
for organism in listOfOrganisms:
	os.system("wget " + organism.genomeFTP)
	os.system("wget " + organism.featureFTP)
	os.system("wget " + organism.transcriptomeFTP)


## Unzips everything in the directory.
os.system('gunzip *.gz')

## Opens a log file to write to
file = open("UPEC.log", 'w+')

## A function that will calculate the number of BP's in the genome file(FASTA format) of the genome of interest. It will also calculate the number of contigs. This data is outputted to the log file.
def contigsBP(genomeFile, organism):
	countContig = 0
	countBP = 0
	for seq_record in SeqIO.parse(genomeFile, "fasta"):
		countContig += 1 
		lengthOfContig = len(str(seq_record.seq))
		if (lengthOfContig > 1000):
			countBP += lengthOfContig
	file.write("There are " + str(countContig) + " contigs in the assembly " + organism.name + "\n")
	file.write("There are " + str(countBP) + " bp in the assembly " + organism.name + "\n")

## This function calls Prokka with the parameter genus specified in the argument. The output directory is the organism name in the first column of the file.
def doProkka(organism, genomeName):
	os.system("prokka --outdir  " + organism.name + " " + "--usegenus --genus " + args.genus + " " + genomeName +"\n")
	file.write("prokka --outdir " + organism.name + " " + "--usegenus --genus " + args.genus + " " + genomeName +"\n")

##This will output the assembly data summary that prokka made to the log file and note any discrepanices between the tRNA value and the CDS value relative to the RefSeq annotation specified in the input file. This is written to the log file.
## Assembly is actually the organismName(for example HM27), featureFileName is the ftpLocation of the featureFile for that organism.
def getDifferences(assembly, featureFileName):
	os.chdir(assembly)
	os.system("mv *.txt " + assembly + "Summary.txt")
	os.chdir("..")
	os.system("mv " + featureFileName + " " + assembly)
	os.chdir(assembly)
	filename = assembly + "Summary.txt"
	with open(filename) as theFile:
		data = [item.strip() for item in theFile.readlines()]
		file.write("Data for assembly " + assembly + ":" + "\n" + "\n")
		for line in data:
			file.write(line +  "\n")

		tRNA = ''
		CDS = ''
		for item in data:
			if ("CDS" in item):
				CDS = item

			if ("tRNA" in item):
				tRNA = item

		predtRNA = int(re.findall('\d+', tRNA)[0])
		predCDS = int(re.findall('\d+', CDS)[0])

	lines = []
	with open(featureFileName) as tsv:
		for line in csv.reader(tsv, delimiter ="\t"):
			lines.append(line)
	
	actualtRNA = int(lines[-2][-1])
	actualCDS = int(lines[1][-1])
	wordOne = "additional"
	wordTwo = "additional"
	tRNAdifference = abs(actualtRNA - predtRNA)
	CDSdifference = abs(actualCDS - predCDS)
	if (predCDS < actualCDS):
		wordOne = "less"

	if (predtRNA < actualtRNA):
		wordTwo = "less"

	booleanCheck = (tRNAdifference == 0) and (CDSdifference == 0)
	if (booleanCheck == False):
		file.write("Prokka found " + str(CDSdifference) + " " + wordOne + " CDS and " + str(tRNAdifference) + " " + wordTwo + " tRNA than the RefSeq in aseembly " + assembly + "\n" + "\n")

	os.chdir("..")

## This will rename the SRA files to organismName.sra Fastq-dump will be done to produce two paired end fastq files that can be used by Tophat in the pipeline.
## The organism is an organism object. The fileName is the fileName of the transcriptome of the organism in SRA format. 
def fastQ(organism, fileName):
	os.system("mv " + fileName + " " + organism.name + ".sra")
	os.system("fastq-dump -I --split-files " + organism.name + ".sra")

### This will take an organismName as a parameter(for example HM27). Bowtie2-build will build an index from the necessary files from beforehand in the pipeline. Tophat2 will run using this index file.
### A -G flag is ommited because it causes numerous errors. Samtools is used to attempt to sort the BAM files. Cufflinks is then run on the BAM files using a -G gff flag.
### **** IMPORTANT with the -G flag cufflinks will not do novel isoform discovery. However, if the -g flag is used cufflinks will do novel isoform discovery.*** YOU CAN MODIFY THIS in the code below by 
### changing the line that says cufflinks with a -G to a -g
def topHatCuffLinks(organismName):
	os.system("bowtie2-build -f " + organismName + ".fa " + organismName)
	os.system("tophat2 -p 2 -o " + organismName + "Out " + organismName + " " + organismName + "_1.fastq " + organismName + "_2.fastq")
	os.system("samtools sort -o " + organismName + ".sorted.bam " + organismName + "Out/accepted_hits.bam")
	os.system("cufflinks -p 2 -G " + organismName + ".gff -o " + organismName + "clOut " + organismName + ".sorted.bam")



superstring = 'cuffnorm merged_asm/merged.gtf '


### This runs the entire pipeline. Rsplit is used to get the exact fileName from the FTP locations. For example ftp://yourlocation/name/name2/file.sra. This will be parsed for file.sra
### File's are renamed to the organismName.fileEnding(for example HM27.sra, HM27.gff) with the mv command by a call to os.system. Then the pipeline is run. The pipeline works until cuffnorm is called outside of this loop.
### ***IMPORTANT: The pipeline works until cuffnorm. After that the pipeline gives a sorted read error***  All other files should be present. 
 
with open("assemblies.txt", 'w+') as fileTwo:
	for organism in listOfOrganisms:
		genomeName = organism.genomeFTP.rsplit('/', 1)[-1][:-3]
		featureName = organism.featureFTP.rsplit('/', 1)[-1][:-3]
		sraName = organism.transcriptomeFTP.rsplit('/', 1)[-1]
		os.system("mv " + genomeName + " " + organism.name + ".fa")
		genomeName = organism.name + ".fa"
		contigsBP(genomeName, organism)
		doProkka(organism, genomeName)
		os.system("mv " + organism.name + "/*.gff " + organism.name + ".gff")
		getDifferences(organism.name, featureName)
		fastQ(organism, sraName)
		topHatCuffLinks(organism.name)
		fileTwo.write("./" + organism.name + "clOut/transcripts.gtf")
		fileTwo.write("/n")
		superstring = superstring +  organism.name + ".sorted.bam "

os.system("cuffmerge -p 2 assemblies.txt") 
os.system(superstring)

file.close()
