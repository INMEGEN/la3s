import csv
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


with open("%s/segmentos.csv" % data_dir, 'w') as f:
    segwriter = csv.writer(f, delimiter="\t")
    segwriter.writerow(["iid","chr","start","nat"])
    for pos in sorted(joint):
        (iid, chrom, start) = pos
        segwriter.writerow([ iid,
                             chrom, 
                             start,
                             (joint[pos]['A'] + joint[pos]['B'] )/ 2])


