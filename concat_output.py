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


for locus in sorted(strloci):
    (chrom, offset) = [int(n) for n in locus.split(":")]

    for ethn in config.inputs.keys():
        with open("%s_detail.txt" % ethn, "a") as detailf:
            with open("run1/la3s_%s_%s/%s_4_detail.txt" % (chrom, offset, ethn), "r") as f:
                for l in f.readlines():
                    if l.startswith('rs'):
                        detailf.write(l)
            
        
    
