import argparse
import json
import csv
import sys

parser = argparse.ArgumentParser(description='Assemble covariates file for given segment.')
parser.add_argument('--segments',  type=argparse.FileType('r'), required=True, help='segments.json file')
parser.add_argument('--covariates', type=argparse.FileType('r'), required=True, help='covariates file')
parser.add_argument('--locus', required=True, help='chrom:offset')
parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)

args = parser.parse_args()

segments = json.load(args.segments)
covreader = csv.reader(args.covariates, delimiter=" ")
covwriter = csv.writer(args.output, delimiter=" ")

covariates = {}
for row in covreader:
    row.remove('')
    covwriter.writerow(row + [segments[args.locus][row[1]],])
