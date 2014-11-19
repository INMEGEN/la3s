
import argparse

parser = argparse.ArgumentParser(description='Average ancestry of both parents')
parser.add_argument('--id', required=True, help='ID of the individual, will read files for A and B')
parser.add_argument('--chr', required=True, help='chromosome to process')

args = parser.parse_args()

joint = {}
for parent in ('A','B'):
    with open("%s_%s_%s.bed.txt" % (args.chr, args.id, parent)) as f:
        lines = f.readlines()
        for line in lines[1:]:
            columnas = line.split()
            (chrom, start, percentage) = (columnas[0], columnas[1], columnas[-1])
            start = int(start)
            if (chrom,start) in joint:
                joint[(chrom,start)][parent] = float(percentage)
            else:
                joint[(chrom,start)] = {parent: float(percentage)}



with open("%s_%s_joint.csv" % (args.chr, args.id), 'w') as f:
    f.write("Chr\tStart(bp)\tNAT\n")
    for pos in sorted(joint):
        (chrom, start) = pos
        f.write("%s\t%s\t%s\n" % (chrom, str(start), (joint[pos]['A'] + joint[pos]['B'] )/ 2))
