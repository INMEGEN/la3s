'''
Genome Wide Imputation
======================

# Dependencies

##  IMPUTE2
https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#download

##  GTOOL
http://www.well.ox.ac.uk/~cfreeman/software/gwas/gtool.html

## 1000 GENOMES (REFERENCE POPULATION)
https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#reference

## Input files
- INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.ped
- INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map
- logHDL_GWAS.fam
- logLDL_GWAS.fam
- logTG_GWAS.fam
- covariables+IMC_GWAS.txt

'''
import subprocess
from subprocess import STDOUT
import argparse
import os
import logging
import sys

parser = argparse.ArgumentParser(description='Impute')

parser.add_argument('--chr', choices=[str(i) for i in range(1,23)], required=True, help="chromosome")
parser.add_argument('--start', required=True)
parser.add_argument('--end', required=True)
parser.add_argument('--ped', required=True)
parser.add_argument('--map', required=True)
parser.add_argument('--hdlfam', required=True)
parser.add_argument('--ldlfam', required=True)
parser.add_argument('--cov', required=True)
parser.add_argument('--combined_mask', required=True, help='/path/to/genetic_map_chr%s_combined_b37.txt')
parser.add_argument('--hap_mask', required=True, help='/path/to/1000GP_Phase3_chr%s.hap.gz')
parser.add_argument('--legend_mask', required=True, help='/path/to/1000GP_Phase3_chr%s.legend.gz')
parser.add_argument('--outdir', required=True, help='no trailing slash!')
parser.add_argument('--log', type=argparse.FileType('w'), default=sys.stdout)    

args = parser.parse_args()

logfile = args.log.name
args.log.close()
logging.basicConfig(filename=logfile, level=logging.DEBUG)

os.chdir(args.outdir)

gtool   = '/home/rgarcia/software/gtool'
impute2 = '/home/rgarcia/software/impute_v2.3.2_x86_64_static/impute2'
plink   = '/usr/bin/p-link'

GEN    = args.outdir + '/' + os.path.split(args.map)[1][:-4] + '.gen'
SAMPLE = args.outdir + '/' + os.path.split(args.map)[1][:-4] + '.sample'

# Format plink files for gtool, if they don't yet exist
if not os.path.isfile(GEN) and not os.path.isfile(SAMPLE):
    logging.debug('Running GTOOL')
    gtool_out = subprocess.check_output(
        [ gtool, '-P',
          '--ped', args.ped,
          '--map', args.map,
          '--og', GEN,
          '--os', SAMPLE ], stderr=STDOUT)
    logging.debug(gtool_out)

# prephase
prephased = args.outdir + '/impute_' + args.chr + '_' + args.start + '_' + args.end + '.prephased'
combined  = args.combined_mask % args.chr
logging.debug('Running prephase')
prephase_out = subprocess.check_output(
    [ impute2, '-prephase_g',
      '-m', combined,
      '-g', GEN,
      '-int', args.start, args.end,
      '-allow_large_regions',
      '-o', prephased ], stderr=STDOUT)
logging.debug(prephase_out)


# impute
imputed  = prephased.replace('.prephased', '.imputed')
hap      = args.hap_mask % args.chr
legend   = args.legend_mask % args.chr
logging.debug('Running impute2')
impute_out = subprocess.check_output(
    [ impute2, '-use_prephased_g',
      '-m', combined,
      '-h', hap,
      '-l', legend,
      '-known_haps_g', prephased + '_haps',
      '-int', args.start, args.end,
      '-allow_large_regions',
      '-Ne', '20000',
      '-o', imputed ], stderr=STDOUT )
logging.debug(impute_out)



# convert impute output to plink map file
imputed_map = imputed.replace('.imputed', '_imputed.map')
imputed_lines = open( imputed + '_info', 'r').readlines()
logging.debug('Converting impute output to plink map')
f = open( imputed_map, 'w')
for l in imputed_lines[1:]:
    fields = l.split()
    snpid = fields[1]
    if snpid.startswith('rs'):
        subfields = snpid.split(':')
        snpid = subfields[0]

    f.write("1\t%s\t0\t%s\n" % (snpid, fields[2]))
f.close()


# plink HDL analysis
hdl_assoc = imputed.replace('.imputed', '_hdl')
logging.debug('Running HDL plink')
hdl_plink_out = subprocess.check_output( [
    plink, '--noweb',
    '--dosage', imputed, 'noheader', 'skip0=1', 'skip1=1', 'format=3',
    '--fam', args.hdlfam,
    '--map', imputed_map,
    '--covar', args.cov,
    '--allow-no-sex',
    '--linear',
    '--out', hdl_assoc,
    '--ci', '0.90'], stderr=STDOUT)
logging.debug(hdl_plink_out)


#### LDL
ldl_assoc = imputed.replace('.imputed', '_ldl')
logging.debug('Running LDL plink')
ldl_plink_out = subprocess.check_output( [
    plink, '--noweb',
    '--dosage', imputed, 'noheader', 'skip0=1', 'skip1=1', 'format=3',
    '--fam', args.ldlfam,
    '--map', imputed_map,
    '--covar', args.cov,
    '--allow-no-sex',
    '--linear',
    '--out', ldl_assoc,
    '--ci', '0.90'], stderr=STDOUT)
logging.debug(ldl_plink_out)
