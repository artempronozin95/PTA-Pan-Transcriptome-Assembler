import os
import pandas as pd
import subprocess
import sys


def hisat_idx(x):
    out = x.rsplit("/", 1)
    out = out[0] + "/hisat_idx"
    inx = "hisat2-build {ref} {out}". format(ref = x, out = out )
    subprocess.call(inx, shell=True)
    return out

def hisat2(t, indx):
    if str(t)[1:-1]  == 'single':
        read = row[0]
        name = read.split("/")
        ID = name[-1].split(".")
        his = "hisat2 -p 32 -x {idx} -S {out} -U {read}". format(idx=indx, out= os.path.join("05_hisat/" + ID + ".sam"), read=read)
        subprocess.call(his, shell=True)
    if str(t)[1:-1] == 'paried':
        read1 = row[0]
        read2 = row[1]
        name = read1.split("/")
        ID = name[-1].split("_")
        his = "hisat2 -p 32 -x {idx} -S {out}  -1 {read_1} -2 {read_2}". format(idx = indx, out= os.path.join("05_hisat/" + ID[0] + ".sam "), read_1=read1, read_2=read2)
        subprocess.call(his, shell=True)
    
    
    
type = sys.argv[1]

files = pd.read_csv(sys.argv[2], sep='\t', header=None)
for index, row in files.iterrows():
    idx = hisat_idx(sys.argv[3])
    mapping = hisat2(type, idx)
