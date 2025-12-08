## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Input](#input)
* [Data](#data)
  * [Configuration](#configuration-file)
  * [Folders](#folders)
* [Running the pipeline](#work-start)
* [Models](#models)
* [Structure information](#lncrna-structure-information)
* [Known LncRNA](#known-lncrna-for-database)
* [Species](#species)
* [Tissue analysis](#tissue-analysis)
* [Expression and entropy](#expression-and-entropy)
* [Output](#output)
* [Errors](#errors)
## Introduction
The pan-genome concept encompasses protein-coding gene sequences subject to presence-absence variations (PAVs) among multiple accessions of a species, some of which may be absent in the reference sequence. In some cases, the plant pan-transcriptome may serve as an approximation of the pan-genome. It is defined as genes expressed across a set of accessions of a species. This approach considers expression-based presence-absence variations (ePAVs). Nevertheless, structural features of pan-genomes and pan-transcriptomes show close correspondence. We present software that allows pan-transcriptome assembly from scratch using only raw read data.

#### This pipeline is only applicable to the Linux operating system.

## Installation
# Automatic
**recommended for clusters/servers**

Install only **assembly.yaml** environment. Other environments will install automatically when **PTA** start work.
```
1. wget https://github.com/artempronozin95/ICAnnoLncRNA-identification-classification-and-annotation-of-LncRNA/archive/refs/heads/main.zip
2. unzip main.zip
3. cd ./ICAnnoLncRNA-identification-classification-and-annotation-of-LncRNA-main
4. conda env create --file env/programs.yaml
5. conda activate ICAnnoLncRNA
```
After these steps all necessary packages are installed. If you need update packages (**not recommended**), change the version of  packages after “=” (example - `snakemake=4.0.1 -> snakemake=6.0.0`), then `conda env update --file ./programs.yaml`. All necessary packages will be updated. Recomended on clusters, requires a lot of  processing power.
# Step method
**recommended for personal computer**
```
1. conda update conda.
2. conda create -n ICAnnoLncRNA python=3.6
3. conda activate ICAnnoLncRNA
4. conda install -c bioconda emboss
5. install next packeges from file below
```
