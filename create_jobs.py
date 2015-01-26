from jinja2 import Template
import json
import os

import config 

la3sdir = os.path.split(os.path.realpath(__file__))[0]

segment_template = Template(open(la3sdir + '/per_segment.template','r').read())

with open("%s/segments.json" % config.data_dir,'r') as f:
    segments = json.load(f)


loci = segments.keys()

# zero pad chromosomes and offsets for sort
strloci = []
for locus in loci:
    (chrom, offset) = locus.split(":")
    strloci.append("%02d:%010d" % (int(chrom), int(offset)))



for i in range(0,len(strloci)):
    (chrom, from_bp)    = [int(n) for n in strloci[i].split(":")]

    # last segments of chromosomes or end of file
    to_bp = config.last_pos[chrom]

    if i < len(strloci)-1:
        (next_chrom, to_bp) = [int(n) for n in strloci[i+1].split(':')]
        # segment in the middle
        if chrom == next_chrom:
            to_bp -=  1

            
    with open("%s_%s.job" % (chrom,from_bp), "w") as f:
        f.write( segment_template.render( plink   = config.plink,
                                          emmax   = config.emmax,
                                          metal   = config.metal,
                                          python  = config.python,
                                          rundir  = config.rundir,
                                          la3sdir = la3sdir,
                                          inputs     = config.inputs,
                                          segments = "%s/segments.json" % config.data_dir,
                                          chrom      = chrom,
                                          from_bp    = from_bp,
                                          to_bp      = to_bp, ) )
        os.chmod(f.name, 0755)
            




