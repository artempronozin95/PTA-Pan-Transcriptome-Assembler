import pandas as pd
# read config info into this namespace
configfile: "config.yaml"

rule all:
    input:
      "02_fastp_results/file_list.txt",
      "configs/all_configs.txt",
      "configs/hisat2.txt",
      "configs/trinity.txt",
      "configs/list_sam.txt",
      "merged.bam",
      "configs/spades_res.txt",
      "07_trinity_gg/trinity/Trinity-GG.fasta",
      "combined/combined.tr",
      "tr2aacds.log",
      "combined/combined.fa"

rule fastp:
    input:
        ancient(expand("{file}", file=config['zip_fastq']))
    params:
        expand("{reads}", reads=config['reads']),
        expand("{average_qual}", average_qual=config['fastp']['average_qual']),
        expand("{length_required}", length_required=config['fastp']['length_required']),
        expand("{thread}", thread=config['fastp']['thread']),
        expand("{overlap_len_require}", overlap_len_require=config['fastp']['overlap_len_require']),
    output:
        first="02_fastp_results/file_list.txt",
        second="configs/all_configs.txt",
        hisat2="configs/hisat2.txt",
        spades="configs/spades.txt"
    run:
        shell("mkdir 01_filter_reads/")
        shell("mkdir 05_hisat")
        shell("mkdir 04_spades")
        shell("python scripts/fastp.py {input} {output.first} {params}")

rule trinity:
    input:
        "02_fastp_results/file_list.txt"
    params:
        memory = expand("{memory}", memory=config['trinity']['max_memory']),
        CPU = expand("{CPU}", CPU=config['trinity']['CPU']),
        Mode = expand("{Mode}", Mode=config['trinity']['mode']),
        Type = expand("{reads}", reads=config['reads']),
        out = "03_trinity/"
    output:
        "configs/trinity.txt"
    run:
         shell("python scripts/trinity.py {input} {params.memory} {params.CPU} {params.Mode} {params.Type} {params.out}")
         shell("ls ./03_trinity/ > configs/trinity.txt")

rule spades:
    input:
        "configs/spades.txt"
    params:
        Type = expand("{reads}", reads=config['reads']),
        out = "04_spades/"
    output:
        "configs/spades_res.txt"
    run:
         shell("python scripts/spades.py {input} {params.Type} {params.out}")
         shell("ls ./04_spades/ > configs/spades_res.txt")

rule hisat2:
     input:
        "configs/hisat2.txt",
        expand("{reference}", reference=config['reference'])
     params:
        expand("{reads}", reads=config['reads'])
     output:
        "configs/list_sam.txt"
     run:
        shell("mkdir 06_hisat_proc/")
        shell("python scripts/hisat.py {params} {input}")
        shell("ls 05_hisat/*.sam > configs/list_sam.txt")

rule samtools: 
    input:
       list="configs/list_sam.txt",
       ref=expand("{reference}", reference=config['reference'])
    params:
       expand("{thr}", thr=config['samtools']['thr'])
    output:
       "merged.bam"
    run:
       files = pd.read_csv(input.list, header=None)
       bam = []
       for w in files[0]:
           arr = w.split(".")
           name = arr[0].split("/")
           fil = arr[0]
           fel = fil + ".bam"
           sor = "06_hisat_proc/" + name[1] + "_sort.bam"
           bam.append(sor)
           shell("samtools view -@ {params} -T {input.ref} -o {fel} {fil}.sam")
           shell("samtools sort -@ {params} --reference {input.ref} {fel} > {sor}")
           shell("samtools stats -@ {params} --reference {input.ref} {sor} > {fil}_samstat.txt")
           shell("samtools index {sor}")
       shell("samtools merge -@ {params} --reference {input.ref} merged.bam {bam}")

rule trinity_GG:
    input:
        "merged.bam"
    params:
       intron=expand("{genome_guided_max_intron}", genome_guided_max_intron=config['trinity']['genome_guided_max_intron']),
       CPU=expand("{CPU}", CPU=config['trinity']['CPU'])
    output:
        "07_trinity_gg/trinity/Trinity-GG.fasta"
    shell:
        "Trinity --max_memory 200G --CPU {params.CPU} --genome_guided_bam {input} --genome_guided_max_intron {params.intron} --output 07_trinity_gg/trinity/"
           

rule combine:
     input:
         spades = "configs/spades_res.txt",
         trinity = "configs/trinity.txt",
         trinityGG = "07_trinity_gg/trinity/Trinity-GG.fasta",
     params:
         Mode = expand("{Mode}", Mode=config['trinity']['mode']),
     output:
         "combined/combined.tr"
     run:
        if params.Mode[0] == "each":
            shell("python scripts/config.py {input.trinity} {input.spades} {input.trinityGG}")
        if params.Mode[0] == "file":
            shell("python scripts/config.py {input.trinity} {input.spades} {input.trinityGG}")
 
rule vsearch:
   input:
      "combined/combined.tr"
   output:
      "combined/combined.fa"
   run:
      shell("vsearch --threads 30 --minseqlength 28 --cluster_fast  {input} --id 0.95 --alnout combined/combined.aln --centroids combined/combined.fa") 
           
rule evi:
   input:
      "combined/combined.fa"
   output:
      "tr2aacds.log"
   run:
      shell("mkdir evi")
      shell("./evigene/scripts/prot/tr2aacds.pl -cdnaseq {input} -logfile ./tr2aacds.log -MINAA 20 -NCPU=32 -MAXMEM=60000")
      shell("mv okayset/ evi")
      shell("mv dropset/ evi")
      shell("mv inputset/ evi")
      shell("mv tmpfiles/ evi")
      

    
       
        
