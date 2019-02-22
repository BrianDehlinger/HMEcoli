import os
from Bio import SeqIO
import logging
import re
import csv


##DEBUG 
## The following gets all of the files necessary for the script to run properly. 


getHM27 = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/825/GCF_000387825.2_ASM38782v2/GCF_000387825.2_ASM38782v2_genomic.fna.gz'
getHM46 = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/845/GCF_000387845.2_ASM38784v2/GCF_000387845.2_ASM38784v2_genomic.fna.gz'
getHM65 = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/785/GCF_000387785.2_ASM38778v2/GCF_000387785.2_ASM38778v2_genomic.fna.gz'
getHM69 = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/865/GCF_000387865.2_ASM38786v2/GCF_000387865.2_ASM38786v2_genomic.fna.gz'

getHM26Features = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/825/GCF_000387825.2_ASM38782v2/GCF_000387825.2_ASM38782v2_feature_count.txt.gz'
getHM46Features = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/845/GCF_000387845.2_ASM38784v2/GCF_000387845.2_ASM38784v2_feature_count.txt.gz'
getHM65Features = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/785/GCF_000387785.2_ASM38778v2/GCF_000387785.2_ASM38778v2_feature_count.txt.gz'
getHM69Features = 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/387/865/GCF_000387865.2_ASM38786v2/GCF_000387865.2_ASM38786v2_feature_count.txt.gz'



## Makes a directory to store all the files in and moves into that directory.


os.system("mkdir temporaryE")
os.chdir("temporaryE")
os.system(getHM27)
os.system(getHM46)
os.system(getHM65)
os.system(getHM69)
os.system(getHM27Features)
os.system(getHM46Features)
os.system(getHM65Features)
os.system(getHM69Features)
os.system('gunzip *.gz')

file = open("UPEC.log", 'w+')



## The following code segment parses the contigs file from NCBI's assembly database for the four bacteria of interest. It writes out the number of contigs and the number of #
## basepairs in the assembly


countHM27 = 0
countBPHM27 = 0
for seq_record in SeqIO.parse("GCF_000387825.2_ASM38782v2_genomic.fna", "fasta"):
	countHM27 += 1
	lengthOfContig = len(str(seq_record.seq))
	if (lengthOfContig > 1000):
		countBPHM27 += lengthOfContig

file.write("There are " + str(countHM27) + " contigs in the assembly HM27" + "\n")
file.write("There are " + str(countBPHM27) + " bp in the assembly HM27" + "\n")

countHM46 = 0
countBPHM46 = 0
for seq_record in SeqIO.parse("GCF_000387845.2_ASM38784v2_genomic.fna", "fasta"):
	countHM46 += 1
	lengthOfContig = len(str(seq_record.seq))
	if (lengthOfContig > 1000):
		countBPHM46 += lengthOfContig

file.write("There are " + str(countHM46) + " contigs in the assembly HM46" + "\n")
file.write("There are " + str(countBPHM46) + " bp in the assembly HM46" + "\n")


countHM65 = 0
countBPHM65 = 0
for seq_record in SeqIO.parse("GCF_000387785.2_ASM38778v2_genomic.fna", "fasta"):
	countHM65 += 1 
	lengthOfContig = len(str(seq_record.seq))
	if (lengthOfContig > 1000):
		countBPHM65 += lengthOfContig

file.write("There are " + str(countHM65) + " contigs in the assembly HM65" + "\n")
file.write("There are " + str(countBPHM65) + " bp in the assembly HM65" + "\n")



countHM69 = 0
countBPHM69 = 0
for seq_record in SeqIO.parse("GCF_000387865.2_ASM38786v2_genomic.fna", "fasta"):
	countHM69 += 1 
	lengthOfContig = len(str(seq_record.seq))
	if (lengthOfContig > 1000):
		countBPHM69 += lengthOfContig

file.write("There are " + str(countHM69) + " contigs in the assembly HM69" + "\n")
file.write("There are " + str(countBPHM69) + " bp in the assembly HM69" + "\n")

## Now we will use Prokka to annotate the assemblies. The code produces an output folder for each strain we are looking at. Prokka is using a genus database to ## speed up assembly. This will produce a folder specified in the outdir flag with the results. There is a log file. 

os.system("prokka --outdir HM27  --usegenus --genus Escherichia GCF_000387825.2_ASM38782v2_genomic.fna")
os.system("prokka --outdir HM46  --usegenus --genus Escherichia GCF_000387845.2_ASM38784v2_genomic.fna")
os.system("prokka --outdir HM65  --usegenus --genus Escherichia GCF_000387785.2_ASM38778v2_genomic.fna")
os.system("prokka --outdir HM69  --usegenus --genus Escherichia GCF_000387865.2_ASM38786v2_genomic.fna")

file.write("These prokka commands were run: " + "\n" + "\n")

file.write("prokka --outdir HM27  --usegenus --genus Escherichia GCF_000387825.2_ASM38782v2_genomic.fna" + "\n")
file.write("prokka --outdir HM46  --usegenus --genus Escherichia GCF_000387845.2_ASM38784v2_genomic.fna" + "\n")
file.write("prokka --outdir HM65  --usegenus --genus Escherichia GCF_000387785.2_ASM38778v2_genomic.fna" + "\n")
file.write("prokka --outdir HM69  --usegenus --genus Escherichia GCF_000387865.2_ASM38786v2_genomic.fna" + "\n")



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


getDifferences("HM27", "GCF_000387825.2_ASM38782v2_feature_count.txt")
getDifferences("HM46", "GCF_000387845.2_ASM38784v2_feature_count.txt")
getDifferences("HM65", "GCF_000387785.2_ASM38778v2_feature_count.txt")
getDifferences("HM69", "GCF_000387865.2_ASM38786v2_feature_count.txt")



file.close()






