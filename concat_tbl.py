import json
import os

import config 

la3sdir = os.path.split(os.path.realpath(__file__))[0]


with open("%s/segments.json" % config.data_dir,'r') as f:
    segments = json.load(f)

loci = segments.keys()

# zero pad chromosomes and offsets for sort
strloci = []
for locus in loci:
    (chrom, offset) = locus.split(":")
    strloci.append("%02d:%010d" % (int(chrom), int(offset)))

header = "MarkerName      Allele1 Allele2 Freq1   FreqSE  MinFreq MaxFreq Effect  StdErr  P-value Direction\n"
    
for ethn in config.inputs.keys():
    with open("%s.tbl" % ethn, "a") as tblf:
        tblf.write(header)
        for locus in sorted(strloci):
            (chrom, offset) = [int(n) for n in locus.split(":")]
            with open("runHDL/la3s_%s_%s/%s_%s1.tbl" % (chrom, offset, chrom, offset), "r") as f:
                for l in f.readlines():
                    if l.startswith('rs'):
                        tblf.write(l)
            
