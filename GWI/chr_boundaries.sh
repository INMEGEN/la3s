for chr in {1..22}
do
    awk '{print "chr"$1,$4}' INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map  | grep -w chr$chr | head -n 1
    awk '{print "chr"$1,$4}' INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map  | grep -w chr$chr | tail -n 1
done
