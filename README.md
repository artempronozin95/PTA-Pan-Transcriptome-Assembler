## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Input](#input)
* [Data](#data)
  * [Configuration](#configuration-file)
* [Run](#Run)
 
## Introduction
The pan-genome concept encompasses protein-coding gene sequences subject to presence-absence variations (PAVs) among multiple accessions of a species, some of which may be absent in the reference sequence. In some cases, the plant pan-transcriptome may serve as an approximation of the pan-genome. It is defined as genes expressed across a set of accessions of a species. This approach considers expression-based presence-absence variations (ePAVs). Nevertheless, structural features of pan-genomes and pan-transcriptomes show close correspondence. We present software that allows pan-transcriptome assembly from scratch using only raw read data.

#### This pipeline is only applicable to the Linux operating system.

The pipeline includes the following steps: 
#### 1. Filtering
#### 2. Assembly.
+ Trinity
+ Trinity Genome guided
+ Spades rna
#### 3. Meta-assembly.
#### 4. Pan-transcriptome assembly

## Installation
# Automatic
**recommended for clusters/servers**

Install only **assembly.yaml** environment. Other environments will install automatically when **PTA** start work.
```
1. wget https://github.com/artempronozin95/PTA-Pan-Transcriptome-Assembler/archive/refs/heads/main.zip
2. unzip main.zip
3. cd ./PTA-Pan-Transcriptome-Assembler
4. conda env create --file env/assembly.yaml
5. conda activate Assembly
```
After these steps all necessary packages are installed. If you need update packages (**not recommended**), change the version of  packages after “=” (example - `snakemake=4.0.1 -> snakemake=6.0.0`), then `conda env update --file ./programs.yaml`. All necessary packages will be updated. Recomended on clusters, requires a lot of  processing power.
# Step method
**recommended for personal computer**
```
1. conda update conda.
2. conda create -n Assembly python=3.6
3. conda activate Assembly
4. conda install -c bioconda emboss
5. install next packeges from assembly.yaml file 
```

## Input
### Raw reads
1. Paried or Single.
### Reference genome
1. Reference genome of the species in `FASTA` format.
2. Annotation of the species in `GFF/GTF` format.

## Data
### Configuration file
Input all necessary files into configuration file “config.yaml”:
+ `lnc:` - known LncRNA sequences of studied organisms in `FASTA` format. 
  + (Example: `lnc: "data/input/lincrna.fasta"`)
+ `reads:` - Need too choose "paried" or "single" reads.
  + (Example: `reads: "paried"`)
+ `zip_fastq:` - path to raw reads files.
  + (Example: `zip_fastq: "./Assambly_pipeline/"`)
+ `fastp:` - Parameters of filtration 
  + `average_qual: 0`
  + `length_required: 5` 
  + `thread: 1`
  + `overlap_len_require: 2`
+ `trinity:` - Parameters of Trinity assembly
  + `mode: "each"` - input "each" of "file"
  + `max_memory: "10G"`
  + `CPU: 2`
  + `genome_guided_max_intron: 500000`
+ `reference:` - Path and name of reference genome
  + (Example: `reference: "ref/GCF_000186305.1_Python_molurus_bivittatus-5.0.2_genomic.fna"`) 
+ `samtools:`
  + `thr: 2`

## Run
### Input Data Preparation
Place all raw read libraries in the **00_raw_reads directory**. Load the reference genome and its annotation into the ref directory.
### Configuration
Before running the pipeline, specify all parameters in the config.yaml file. Parameters are organized into blocks labeled by program names. The library type must be specified as either "paired" or "single".​
### Execution
To run the pipeline, execute the following command:​
```
snakemake -j 1    # Sequential processing
snakemake -j 2    # Parallel processing with 2 threads (or 3, 4, etc.)
```
### Pipeline Stages
+ Stage 1: Quality control is performed and configuration files are generated for all assemblers. Configuration files are written to the configs directory. The following directories are created: 01_filter_reads, 02_fastp_results, 04_soap, 05_hisat.
+ Stage 2: Processes are independent and can be run in parallel by specifying multiple threads (-j 3). The following directories are created: 03_trinity, 04_soap, 05_hisat, 06_hisat_proc. (Note: Is soap.err necessary?)
+ Stage 3: The merged.bam file is created in the root directory (suggestions for alternative directory location?) and the 07_trinity_gg directory is generated.


