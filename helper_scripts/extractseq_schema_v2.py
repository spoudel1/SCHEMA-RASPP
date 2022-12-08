#this script will extract sequences based on the chimera library schema generates
#it requires, crossover containing file (should be only one line), multiple sequence alignment file, chimerafile

import sys
import statistics
import argparse


msa={}
nt_seq=[]
msa_order={}
finalmsa=[]
crosspoint=[]

#adding gaps in nt seq
def putgapsinnt(ntseq,nindex):
    new_ntset=''
    nt_count=0
    for x in range(0, len(finalmsa[nindex])):
        if not finalmsa[nindex][x]=='-':
            for i in range(0,3):
                new_ntset+=ntseq[nt_count+i]
            nt_count+=3
        else:
            for i in range(0,3):
                new_ntset+='-'
    return new_ntset

#getting the seq based on crosspoint
def getseq(names, num, crosspoint):
    present=0
    chimera=''
    chimera_nt=''
    clone_index=0
    copying=False
    lastrun=0
    if num==2:
        lastrun=0
        for y in range(0, len(finalmsa[0])):
            if not y == crosspoint[clone_index]:
                if lastrun==1:
                    chimera+=(finalmsa[int(names[clone_index+1])-1][y])
                else:
                     chimera+=(finalmsa[int(names[clone_index])-1][y])
            else:
                if clone_index==len(crosspoint)-1:
                    lastrun=1
                chimera+=(finalmsa[int(names[clone_index])-1][y])
                if clone_index<(len(names)-2):
                    clone_index+=1
        clone_index=0
        lastrun=0
        #for nucleotide
        for y in range(0, len(nt_seq[0]),3):
            if not y == int(crosspoint[clone_index])*3:
                if lastrun==1:
                    for i in range(0,3):
                        chimera_nt+=(nt_seq[int(names[clone_index+1])-1][y+i])
                else:
                    for i in range(0,3):
                        chimera_nt+=(nt_seq[int(names[clone_index])-1][y+i])
            else:
                if clone_index==len(crosspoint)-1:
                    lastrun=1
                for i in range(0,3):
                    chimera_nt+=(nt_seq[int(names[clone_index])-1][y+i])
                if clone_index<(len(names)-2):
                    clone_index+=1
        return chimera,chimera_nt
#        print(chimera, " chimera ", chimera_nt)
#        input()
    elif num==1:
        for y in range(0, len(finalmsa[0])):
            if not y == crosspoint[clone_index]:
                if lastrun==1:
                    chimera+=(finalmsa[int(names[clone_index+1])-1][y])
                else:
                     chimera+=(finalmsa[int(names[clone_index])-1][y])
            else:
                if clone_index==len(crosspoint)-1:
                    lastrun=1
                chimera+=(finalmsa[int(names[clone_index])-1][y])
                if clone_index<(len(names)-2):
                    clone_index+=1
        return chimera

#main loop
def main(argv):
    #Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-x", "--crossover_point", type=str, help="path to the crossover point", required=True, action='store')
    parser.add_argument("-m", "--multiple_align", type=str, help="multiple sequence alignment file", required=True, action='store')
    parser.add_argument("-n", "--ntseq", type=str, help="nucleotide sequence file in the same order as msa file", required=False, action='store')
    parser.add_argument("-e", "--combos", type=str, help="file containing combinations", required=True, action='store')
    parser.add_argument("-o", "--output", type=str, help="outputfile for chimeras (amino acid seq)", required=True, action='store')
    parser.add_argument("-nto", "--nt_output", type=str, help="outputfile for chimeras (nucleotide seq)", required=False, action='store')

    args = parser.parse_args()
    xofile=open(args.crossover_point,'r')
    msafile=open(args.multiple_align,'r')
    if args.ntseq:
        ntfile=open(args.ntseq,'r')
        ntoutputfile=open(args.nt_output,"w")
    chimerafile=open(args.combos,'r')
    outputfile=open(args.output,'w')

    #reading the crossover file and storing the positions
    for xo in xofile:
        xo_strip=xo.strip()
        crosspoint=[int(x) for x in xo_strip.split(' ')]
    xofile.close()
    
    #allowed_chars = set("ACDEFGHIKLMNPQRSTVWY0123456789")
 #   print(crosspoint, 'crosspoint') 
    #reading the multile sequence file
    count=1
    for line in msafile:
        if ":" in line or "." in line or '*' in line:
            continue
        line_split=line.strip().split()
        if line_split:
            if not line_split[0] in msa:
                msa[line_split[0]]=line_split[1]
                msa_order[line_split[0]]=count
                count+=1
            else:
                msa[line_split[0]]+=line_split[1]
    #restoring the msa in the same order as the input
    tcount=1
    for keys, val in msa_order.items():
        if str(val)==str(tcount):
            finalmsa.append(msa[keys])
            tcount+=1
    msa_num=[] #stores msa numbering to actual sequence number
    
    #reading nucleotide sequence
    if args.ntseq:
        copying=False
        seqid=''
        sequences=''
        ncount=0
        for nt in ntfile:
            nt_strip=nt.strip()
            if nt_strip.startswith('>'):
                if copying==True:
                    nt_seq.append(putgapsinnt(sequences, int(ncount)))
                    ncount+=1
                    sequences=''
                seqid=nt_strip[1:]
                copying=True
            elif copying:
                sequences+=nt_strip
        nt_seq.append(putgapsinnt(sequences,int(ncount)))
        #print("ntfile")
        #print(nt_seq)
    
    chim_keys="-".join(k for k in msa.keys()) #get protein id to make chimera from
    disrupte=[]
    clones=[]
    for word in chimerafile:
        word_split=word.strip().split()
        if not '#' in word:
            disrupte.append(int(word_split[1]))    
            clones.append(word_split[0])

    average_disrupte=statistics.mean(disrupte)
    stdev_disrupte=statistics.stdev(disrupte)
    #print(min_score,'score',max_score)

    #printing chimera seqs
    for ts in range(0,len(clones)):
        if disrupte[ts]>=average_disrupte-stdev_disrupte and disrupte[ts]<=average_disrupte+stdev_disrupte:
            if args.ntseq:
                chimera_seq, nt_chimera=getseq(clones[ts],2, crosspoint)
                nt_chimera_filter=nt_chimera.replace("-","")
            else:
                chimera_seq=getseq(clones[ts],1, crosspoint)
            chimera_seq_filter=chimera_seq.replace("-","")
            if not len(chimera_seq_filter)<4:  #this will restrict chimera length to a minimum of 60. Uncomment if you don't want length restriction.
                outputfile.write(">"+chim_keys+"-"+clones[ts]+"-Chimera_seq"+str(ts)+'\n'+chimera_seq_filter+'\n')
                if args.ntseq:
                    ntoutputfile.write(">"+chim_keys+"_"+clones[ts]+"-Chimera_seq"+str(ts)+'\n'+nt_chimera_filter+'\n')
           # input()
    print('Average distribution: ',average_disrupte,' and Standard deviation: ',stdev_disrupte, ' Total number of clones: ', len(clones))

if __name__ =="__main__":
    main(sys.argv[1:])
