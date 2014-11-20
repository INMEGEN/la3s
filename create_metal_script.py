import argparse
from string import Template
import sys

parser = argparse.ArgumentParser(description='create metal script for inputs')
parser.add_argument('--details', nargs='+', required=True, help='one or mor detail files')
parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)

args = parser.parse_args()

head="""SCHEME   STDERR
STDERR SE
GENOMICCONTROL ON
AVERAGEFREQ ON
MINMAXFREQ ON
"""

pop_stanza="""MARKER SNP
ALLELE A1 A2
FREQLABEL MAF
EFFECT BETA
STDERR   SE
PVAL     P
PROCESS $detail
"""
t = Template(pop_stanza)

foot="""OUTFILE metal_outfile.tbl
ANALYZE
QUIT
"""

args.output.write(head)
for f in args.details:
    args.output.write( t.substitute(detail=f) )
args.output.write(foot)

args.output.close()
