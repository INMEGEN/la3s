import argparse
import sys


parser = argparse.ArgumentParser(description='Mark imputed entries in dosage file')

parser.add_argument('--map', type=argparse.FileType('r'), required=True)    
parser.add_argument('--dosage', type=argparse.FileType('r'), required=True)
parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout) 

args = parser.parse_args()

# create set of rsIDs from map file
rsids = []
for l in args.map.readlines():
    fields = l.split()
    rsids.append(fields[1])


# match snp to genotype or not
for l in args.dosage.readlines():
    fields = l.strip().split()
    if fields[1] in rsids:
        mark = 'genotyped'
    else:
        mark = 'imputed'
    fields.append(mark)

    args.output.write( "\t".join(fields) + "\n" )
