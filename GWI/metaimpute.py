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
import argparse
import os

parser = argparse.ArgumentParser(description='Impute')

parser.add_argument('--chr', choices=range(1,23), required=True, help="chromosome")
parser.add_argument('--ped', required=True)
parser.add_argument('--map', required=True)
parser.add_argument('--hdlfam', required=True)
parser.add_argument('--ldlfam', required=True)
parser.add_argument('--cov', required=True)
parser.add_argument('--combined_mask', required=True, help='/path/to/genetic_map_chr%s_combined_b37.txt')
parser.add_argument('--hap_mask', required=True, help='/path/to/1000GP_Phase3_chr%s.hap.gz')
parser.add_argument('--legend_mask', required=True, help='/path/to/1000GP_Phase3_chr%s.legend.gz')
parser.add_argument('--outdir', required=True, help='no trailing slash!')

args = parser.parse_args()

gtool   = '/home/sromero/gtool_v0.7.5_x86_64_dynamic/gtool'
impute2 = '/home/sromero/impute_v2.3.0_x86_64_dynamic/impute2'
plink   = '/home/sromero/plink-1.07-x86_64/plink'

GEN    = args.outdir + '/' + os.path.split(args.map)[1][:-4] + '.gen'
SAMPLE = args.outdir + '/' + os.path.split(args.map)[1][:-4] + '.sample'


# Format plink files for gtool
subprocess.check_output(
    [ gtool, '-P',
      '--ped', args.ped,
      '--map', args.map,
      '--og', GEN,
      '--os', SAMPLE ] )

# prephase
prephased = args.outdir + '/chr' + args.chr + '.prephased'
combined  = args.combined_mask % args.chr
subprocess.check_output(
    [ impute2, '-prephase_g',
      '-m', combined,
      '-g', GEN,
      '-int 1 1000000',
      '-allow_large_regions',
      '-Ne 20000',
      '-o', prephased ] )



# impute
imputed  =  args.outdir + '/chr' + args.chr + '.imputed'
hap      = args.hap_mask % args.chr
legend   = args.legend_mask % args.chr
subprocess.check_output(
    [ impute2, '-use_prephased_g',
      '-m', combined,
      '-h', hap,
      '-l', legend,
      '-known_haps_g', prephased,
      '-int 1 1000000',
      '-allow_large_regions',
      '-Ne 20000',
      '-o', imputed ] )


### ANALISIS DE DATOS IMPUTADOS

#    cat INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large_info | awk '{print "1",$2,"0",$3}' | sed '1d' > INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map


'''
### ANALISIS PLINK

#### HDL

##### CHR 1 HASTA CHR 22
'''
subprocess.check_output( [
    plink, '--noweb',
    '--dosage INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large noheader skip0=1 skip1=1 format=3',
    '--fam logHDL_GWAS.fam',
    '--map INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map',
    '--covar', args.cov,
    '--allow-no-sex',
    '--linear',
    '--out INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.ASSOC',
    '--ci 0.',])



#### LDL
##### CHR 1 HASTA CHR 22
subprocess.check_output( [
    plink, '--noweb',
    '--dosage INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large noheader skip0=1 skip1=1 format=3',
    '--fam logLDL_GWAS.fam',
    '--map INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map',
    '--covar', args.cov,
    '--allow-no-sex',
    '--linear',
    '--out INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.ASSOC',
    '--ci 0.',])
