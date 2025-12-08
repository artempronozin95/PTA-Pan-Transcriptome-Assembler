import os
import glob
import subprocess
import sys
import pandas as pd


def fastp_pair(q,x,y,z,r,e):
     cmd = "fastp -i {read_1} -I {read_2} -o {out_1} -O {out_2} -j {json} -h {html} -e {average_qual} -l {length_required} -w {thread} -c --overlap_len_require {overlap_len_require}". format(read_1=os.path.join(q + x), read_2=os.path.join(q + z + "_2." + e), out_1=os.path.join(y + z + "_1." + e), out_2=os.path.join(y + z + "_2." + e), json=os.path.join(r + z + ".json"), 
     html=os.path.join(r + z + ".html"), average_qual=str(sys.argv[10])[1:-1], length_required=str(sys.argv[11])[1:-1], thread=str(sys.argv[12])[1:-1], overlap_len_require=str(sys.argv[13])[1:-1])
     subprocess.call(cmd, shell=True)
     return print(cmd)
 
def fastp_single(q,x,y,z,r,e):
     cmd = "fastp -i {read_1} -o {out_1} -j {json} -h {html} -e {average_qual} -l {length_required} -w {thread} -c --overlap_len_require {overlap_len_require}". format(read_1=os.path.join(q + x),
     out_1=os.path.join(y + z + "_1." + e), json=os.path.join(r + z + ".json"), html=os.path.join(r + z + ".html"), average_qual=str(sys.argv[10])[1:-1], length_required=str(sys.argv[11])[1:-1], thread=str(sys.argv[12])[1:-1], overlap_len_require=str(sys.argv[13])[1:-1])
     subprocess.call(cmd, shell=True)
     return print(cmd)
   
# fastp run     
path = sys.argv[1]
raw = path + "00_raw_reads/"
filt = path +"01_filter_reads/"
rep = path + "02_fastp_results/"
os.chdir(raw)

files = os.listdir()
col1 = []
col2 = []
read_1 = []
read_2 = []
for lib in files:
  arr = lib.split(".")
  if arr[-1] != "gz":
      end = '.'.join(arr[-1:])	
      brr = arr[0].split("_")
      if str(sys.argv[9])[1:-1] == "paried":
         if brr[-1] != "2":
            col1.append(brr[0])
            col2.append(os.path.join(brr[0] + '_rep1'))
            read_1.append(os.path.join(filt +lib))
            read_2.append(os.path.join(filt + brr[0]+ "_2." + end))
            print(read_1, read_2)
            fastp_pair(raw, lib, filt, brr[0], rep, end)
         else:
            pass
      if str(sys.argv[9])[1:-1] == "single":
         fastp_single(raw, lib, filt, brr[0], rep, end)
  else:
      end = '.'.join(arr[-2:])
      brr = arr[0].split("_")
      if str(sys.argv[9])[1:-1] == "paried":
        if brr[-1] != "2":
           col1.append(brr[0])
           col2.append(os.path.join(brr[0] + '_rep1'))
           read_1.append(os.path.join(filt +lib))
           read_2.append(os.path.join(filt + brr[0]+ "_2." + end))
           fastp_pair(raw, lib, filt, brr[0], rep, end)
        else:
           pass
      if str(sys.argv[9])[1:-1] == "single":
        fastp_single(raw, lib, filt, brr[0], rep, end)

# form sample_file for Trinity
df = pd.DataFrame(list(zip(col1, col2, read_1, read_2)))
df.to_csv(path + sys.argv[2], sep='\t', index=None, header=None)

# form sample_file for hisat2
hisat = pd.DataFrame(list(zip(read_1, read_2)))
hisat.to_csv(path + 'configs/hisat2.txt', sep='\t', index=None, header=None)

# form sample_file for spades
spades = pd.DataFrame(list(zip(col1, read_1, read_2)))
spades.to_csv(path + 'configs/spades.txt', sep='\t', index=None, header=None)


