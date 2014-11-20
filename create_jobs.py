from jinja2 import Template
import json

import config 

segment_template = Template(open('per_segment.template','r').read())

with open("%s/segments.json" % config.data_dir,'r') as f:
    segments = json.load(f)

loci = sorted(segments.keys())

for i in range(0,len(loci)):
    (chrom, from_kb)    = loci[i].split(':')
    (next_chrom, to_kb) = loci[i+1].split(':')
    if chrom == next_chrom:
        print segment_template.render( plink   = config.plink,
                                       emmax   = config.emmax,
                                       metal   = config.metal,
                                       python  = config.python,
                                       inputs     = config.inputs,
                                       segments = "%s/segments.json" % config.data_dir,
                                       chrom      = chrom,
                                       from_kb    = from_kb,
                                       to_kb      = to_kb, )

