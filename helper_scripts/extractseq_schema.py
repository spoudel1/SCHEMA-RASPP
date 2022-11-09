#this script will extract sequences based on the chimera library schema generates
#it requires, crossover containing file (should be only one line), multiple sequence alignment file, chimerafile

import sys
import statistics

xofile=open(sys.argv[1],'r')
msafile=open(sys.argv[2],'r')
chimerafile=open(sys.argv[3],'r')
outputfile=open(sys.argv[4],'w')
crosspoint=[]
msa={}
msa_order={}
for xo in xofile:
    xo_strip=xo.strip()
    crosspoint=[int(x) for x in xo_strip.split(' ')]
#allowed_chars = set("ACDEFGHIKLMNPQRSTVWY0123456789")
count=1
for line in msafile:
    if ":" in line or "." in line:
        continue
    line_split=line.strip().split()
    if line_split:
        if not line_split[0] in msa:
            msa[line_split[0]]=line_split[1]
            msa_order[line_split[0]]=count
            count+=1
        else:
            msa[line_split[0]]+=line_split[1]
#print('Seq in fasta format:')
#print(msa)
#print(msa_order)
disrupte=[]
clones=[]
for word in chimerafile:
    word_split=word.strip().split()
    if not '#' in word:
        disrupte.append(int(word_split[1]))    
        clones.append(word_split[0])


def getseq(names):
    present=0
#    print(names,'pairs')
    msa_seqs=list(msa.values())
    chimera=''
    clone_index=0
    seqpos=0
#    print(names[5],'names', crosspoint[4])
    for y in range(0, len(msa_seqs[0])):
        if not seqpos == crosspoint[clone_index]:
         #   print("first",msa_seqs[int(names[clone_index])-1][y])
            chimera+=(msa_seqs[int(names[clone_index])-1][y])
          #  print(clone_index, names[clone_index])
        else:
           # print("second",msa_seqs[int(names[clone_index])-1][y])
            chimera+=(msa_seqs[int(names[clone_index])-1][y])
          #  print("error here")
            if clone_index<(len(names)-2):
                clone_index+=1
        seqpos+=1
#        print(crosspoint[clone_index],'and ', seqpos, ' what ',clone_index, ' len ',len(names))
#    print ('chimera',chimera)
    return chimera
average_disrupte=statistics.mean(disrupte)
stdev_disrupte=statistics.stdev(disrupte)
min_score=average_disrupte-stdev_disrupte
max_score=average_disrupte+stdev_disrupte
#print(min_score,'score',max_score)
for ts in range(0,len(clones)):
    if disrupte[ts]>average_disrupte-stdev_disrupte and disrupte[ts]<average_disrupte+stdev_disrupte:
        chimera_seq=getseq(clones[ts])
        chimera_seq_filter=chimera_seq.replace("-","")
#        print("getting seq of: ",clones[ts])
#        print(chimera_seq, 'after', chimera_seq_filter)
        outputfile.write(">PS1165-Chimera_seq"+str(ts)+'\n'+chimera_seq_filter+'\n')
       # input()
print('Average distribution: ',average_disrupte,' and Standard deviation: ',stdev_disrupte, ' Total number of clones: ', len(clones))
#print(word_split)
#for key,value in msa.items():
#    outputfile.write(">"+key+'\n'+value+'\n')
