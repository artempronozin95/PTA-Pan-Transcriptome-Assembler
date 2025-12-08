import os
import pandas as pd
import subprocess
import sys

if sys.argv[4] == 'file':
    Trinity = "Trinity --seqType fq --max_memory {memory} --CPU {cpu} --samples_file {sample} --output {out}".format(memory=sys.argv[2],
                                                                                                                     cpu=sys.argv[3],
                                                                                                                     sample=sys.argv[1],
                                                                                                                     out=sys.argv[6])
    subprocess.call(Trinity, shell=True)
if sys.argv[4] == 'each':
    df = pd.read_csv(sys.argv[1], header=None, sep='\t')
    for index, row in df.iterrows():
        out = os.path.join(sys.argv[6], row[0] + '_trinity')
        if sys.argv[5] == 'single':
            Trinity = "Trinity --seqType fq --max_memory {memory} --CPU {cpu} --single {single} --output {out}".format(memory=sys.argv[2],
                                                                                                                   cpu=sys.argv[3],
                                                                                                                   single=row[2],
                                                                                                                   out=out)
            subprocess.call(Trinity, shell=True)
        if sys.argv[5]  == 'paried':
            Trinity = "Trinity --seqType fq --max_memory {memory} --CPU {cpu} --left {left} --right {right} --output {out}".format(memory=sys.argv[2],
                                                                                                                               cpu=sys.argv[3],
                                                                                                                               left=row[2],
                                                                                                                               right=row[3],
                                                                                                                               out=out)
            subprocess.call(Trinity, shell=True)