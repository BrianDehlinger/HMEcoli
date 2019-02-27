# HMEcoli
The repository for the tuxedo package analysis of HM27, HM46, HM65, and HM69 Ecoli strains

## Note this software's genus flag must be one of the genus in your database of genera in Prokka. Details are found in Prokka's doucmentation.

This program is part of a pipeline to identify significant changes in expression between bacterial strains. NCBI's assemblies for these strains are retrieved via the NCBI ftp server using wget. These assemblies are annotated using Prokka to determine what genes could be expressed. Transcriptome data was obtained from NCBI's SRA database again through the ftp server using wget on linux. TopHat is used to map the reads of a strain to that strain's genome. Cufflinks determines the expression of the genes. 

In order to run this program the following must be installed on a Linux Server. The following dependencies are needed:

TopHat2 https://ccb.jhu.edu/software/tophat/index.shtml

Cufflinks v2.2.1 http://cole-trapnell-lab.github.io/cufflinks/

Prokka 1.13 http://www.vicbioinformatics.com/software.prokka.shtml

Biopython https://biopython.org/

Python(version 3 or greater) (3.6.7 used for this project) https://www.python.org/downloads/

Highly Recommended to use a Tmux session or use Nohup so that the jobs finish. 

Steps to Run:
1) Download all of the files or git clone into a directory of choice via the terminal. You can use cd to change into the directory you would like to run the program in.
2) Format your data file containing rows with the organism name, the ftp location of the genome, the ftp location of the transcriptome, and the ftp location of the featureCount file. All of these attributes should be seperated by a single space and in the order described.
2.5) HIGHLY RECOMMENDED: Make sure you are in the working directory you want to run everything in. Type tmux. This will attach you to a tmux session. Then run the following. return to your native terminal by pressing Ctrl+b then d. When you want to see what happens in that terminal again type tmux attach -t 0(or 1 or 2 or 3 and so forth depending on how many other sessions of tmux you have open and which session this is).
3) The program takes 3 input parameters. The path to the data file. A genus to use in Prokka and a name for an output folder.
	In order to run the program here is what the command should look something like this: **Test.txt is your own data file** **Escherichia is the genus** **Dehlinger_Brian will be an output directory in the current working directory**

	python Pipeline.py C:/Users/Documents/Brian/Test.txt Escherichia Dehlinger_Brian

	Or if your machine uses the name python3 for python version 3 or greater.
	
	python3 Pipeline.py C:/Users/Documents/Brian/Test.txt Escherichia Dehlinger_Brian


## How to format your data file(Test.txt):

The Test.txt file is an example of what input to the program should look like. Each line is a sample. The columns are seperated by a single space. The first column contains the name of the Organism/Sample(for example HM27). The second column is the location of the genome fasta file for a bacterial genome.

