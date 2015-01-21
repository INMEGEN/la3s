import json
from string import Template

job = Template('''
Arguments = metaimpute.py \\
          --chr $chr \\
          --start $start \\
          --end $end \\
          --ped /home/rgarcia/la3s/GWI/data/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.ped \\
          --map /home/rgarcia/la3s/GWI/data/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map \\
          --hdlfam /home/rgarcia/la3s/GWI/data/logHDL_GWAS.fam \\
          --ldlfam /home/rgarcia/la3s/GWI/data/logLDL_GWAS.fam \\
          --cov /home/rgarcia/la3s/GWI/data/covariables+IMC_GWAS.txt \\
          --combined_mask /home/rgarcia/la3s/GWI/1000GP_Phase3/genetic_map_chr%s_combined_b37.txt \\
          --hap_mask /home/rgarcia/la3s/GWI/1000GP_Phase3/1000GP_Phase3_chr%s.hap.gz \\
          --legend_mask /home/rgarcia/la3s/GWI/1000GP_Phase3/1000GP_Phase3_chr%s.legend.gz \\
          --outdir /home/rgarcia/la3s/GWI/out \\
          --log /home/rgarcia/la3s/GWI/out/impute_${chr}_${start}_${end}.log
Error = /home/rgarcia/la3s/GWI/out/condor_${chr}_${start}_${end}.log
Requirements = Machine == "gaia.inmegen.gob.mx"
Queue
''')



print "executable = /usr/bin/python"
print "universe = vanilla"

chr_boundaries = json.load(open('chr_boundaries.json','r'))

window = 5000000

for boundary in chr_boundaries:
    chrom = boundary['chr']
    start = boundary['start']
    end   = boundary['end']

    n = start - 10000
    while n < end:
        print job.substitute(chr=chrom, start=n, end=n+window)
        n += window + 1
