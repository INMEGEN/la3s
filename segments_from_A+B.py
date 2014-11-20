
################################################################
# This script will generate a segments file from A+B bed files #
################################################################

import csv
import json

from config import individuals, chromosomes, data_dir

joint = {}
for chrom in chromosomes:
    for iid in individuals:
        for parent in ('A','B'):
            with open("%s/chr%s_out/chr%s_%s_%s.bed.txt" % (data_dir, chrom, chrom, iid, parent)) as f:
                bedreader = csv.reader(f, delimiter="\t")
                header = bedreader.next()
                for row in bedreader:
                    (chrom, start, posterior) = (row[0], row[1], row[-1])
                    (ceu,yri,nat) = posterior.split(',')
                    start = int(start)
                    if (iid,chrom,start) in joint:
                        joint[(iid,chrom,start)][parent] = float(nat)
                    else:
                        joint[(iid,chrom,start)] = {parent: float(nat)}


segments={}
for k in sorted(joint):
    (iid, chrom, start) = k
    pos = "%s:%s" % (chrom, start)
    if not pos  in segments:
        segments[ pos ] = {}
    segments[ pos ][ iid ]= (joint[k]['A'] + joint[k]['B'] )/ 2

with open("%s/segments.json" % data_dir, 'w') as f:
    json.dump(segments, f, indent=4)
