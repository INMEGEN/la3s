from jinja2 import Template
import json
import os

import config 

la3sdir = os.path.split(os.path.realpath(__file__))[0]

segment_template = Template(open(la3sdir + '/per_segment.template','r').read())

with open("%s/segments.json" % config.data_dir,'r') as f:
    segments = json.load(f)

loci = sorted(segments.keys())

for i in range(0,len(loci)-1):
    (chrom, from_bp)    = loci[i].split(':')
    (next_chrom, to_bp) = loci[i+1].split(':')
    to_bp = str(int(to_bp) - 1)
    if chrom == next_chrom:
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

