import os
import pandas as pd
import subprocess
import sys

df = pd.read_csv(sys.argv[1], header=None, sep='\t')
for index, row in df.iterrows():
    out = os.path.join(sys.argv[3], row[0])
    if sys.argv[2] == 'paried':
       Spades = "spades.py --rna -o {out} -1 {right} -2 {left}".format(out=out, right=row[1], left=row[2])
       subprocess.call(Spades, shell=True)
    if sys.argv[2] == 'single':
       Spades = "spades.py --rna -o {out} -s {single}".format(out=out, single=row[1])
       subprocess.call(Spades, shell=True)
