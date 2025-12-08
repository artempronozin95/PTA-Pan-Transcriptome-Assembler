from shutil import copyfile
import subprocess
import pandas as pd
import sys
import os
from glob import glob


def rename(table, dirr, name_file):
    list_files = []
    for w in table[0]:
    #    print(w)
        path = dirr + w + name_file
#        strr = '\'s/>.*/&_' + w + '/\''
#        command = 'sed -i {string} {input}' .\
#           format(string=strr, input=path)
#        subprocess.call(command, shell=True)
        list_files.append(path)
    return list_files


trinity = pd.read_csv(sys.argv[1], sep='\t', header=None)
spades = pd.read_csv(sys.argv[2], sep='\t', header=None)
outfile = ("./combined/combined.tr")

list_trinity = rename(trinity, './03_trinity/', '/Trinity.fasta')
list_spades = rename(spades, './04_spades/', '/transcripts.fasta')


combine = 'evigene/scripts/rnaseq/trformat.pl -output {outdir} -input {trinity} {spades} {trinityGG}' . format(outdir=outfile, trinity=" ".join(list_trinity), spades=" ".join(list_spades), trinityGG=sys.argv[3])
print(combine)
subprocess.call(combine, shell=True)
