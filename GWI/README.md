Genome Wide Imputation
======================


# Dependencies

###  IMPUTE2
https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#download

###  GTOOL

http://www.well.ox.ac.uk/~cfreeman/software/gwas/gtool.html

### 1000 GENOMES (REFERENCE POPULATION)

https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#reference


### ARCHIVOS ADJUNTADOS

- INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.ped
- INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map
- logHDL_GWAS.fam
- logLDL_GWAS.fam
- logTG_GWAS.fam
- covariables+IMC_GWAS.txt

---------------------------------


# Pipeline


### CAMBIAR FORMATO DE ARCHIVO ADJUNTADO CON GTOOL PARA UTILIZAR IMPUTE

#### CHR 16 


    /home/sromero/gtool_v0.7.5_x86_64_dynamic/gtool -P \
    --ped INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.ped \
    --map INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map \
    --og INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map.gen \
    --os INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.sample



### IMPUTACION 1000 GENOMAS

## Imputación con prefaseo

 *-m: Archivo que se obtiene de 1000G de la páina de IMPUTE2
 * -g: Archivo que se obtiene al transformar con GTOOL los archivos .ped y .map
 * -int: Marca el intervalo a analizar, quedÃ³ establecido un intervalo de 1Mb
 * -Ne: Es un valor fijo;



#### CHR 1

#### PREFASEO


    /home/sromero/impute_v2.3.0_x86_64_dynamic/impute2 -prephase_g \
    -m /home/sromero/ALL_1000G_phase1integrated_v3_impute/genetic_map_chr1_combined_b37.txt \
    -g Dropbox/MICROARREGLOS_2014/GWAS_519/IMPUT_GWAS_519/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.map.gen \
    -int 1 1000000 \
    -allow_large_regions \
    -Ne 20000 \
    -o Dropbox/MICROARREGLOS_2014/GWAS_519/IMPUT_GWAS_519/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase

 * -m: Archivo que se obtiene de 1000G de la pÃ¡gina de IMPUTE2
 * -g: Archivo que se obtiene al transformar con GTOOL los archivos .ped y .map
 * -int: Marca el intervalo a analizar, quedÃ³ establecido un intervalo de 1Mb
 * -Ne: Es un valor fijo;


#### IMPUTACION CON PREFASEO

    /home/sromero/impute_v2.3.0_x86_64_dynamic/impute2 -use_prephased_g \
    -m /home/sromero/ALL_1000G_phase1integrated_v3_impute/genetic_map_chr1_combined_b37.txt \
    -h /home/sromero/ALL_1000G_phase1integrated_v3_impute/ALL_1000G_phase1integrated_v3_chr1_impute.hap.gz \
    -l /home/sromero/ALL_1000G_phase1integrated_v3_impute/ALL_1000G_phase1integrated_v3_chr1_impute.legend.gz \
    -known_haps_g Dropbox/MICROARREGLOS_2014/GWAS_519/IMPUT_GWAS_519/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_haps \
    -int 1 1000000 \
    -allow_large_regions \
    -Ne 20000 \
    -o Dropbox/MICROARREGLOS_2014/GWAS_519/IMPUT_GWAS_519/INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large


 * -m: Archivo que se obtiene de 1000G de la pÃ¡gina de IMPUTE2
 * -h: Archivo que se obtiene de 1000G de la pÃ¡gina de IMPUTE2
 * -l: Archivo que se obtiene de 1000G de la pÃ¡gina de IMPUTE2
 * -known_haps_g: Archivo que se obtiene del prefaseo (paso anterior)
 * -int: Marca el intervalo a analizar, quedÃ³ establecido un intervalo de 1Mb
 * -Ne: Es un valor fijo;




### ANALISIS DE DATOS IMPUTADOS



#### HACER EL ARCHIVO .MAP PARA PODER ANALIZAR LOS RESULTADOS

    cat INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large_info | awk '{print "1",$2,"0",$3}' | sed '1d' > INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map



### ANALISIS PLINK

#### HDL


##### CHR 1 HASTA CHR 22

##### ANALISIS CON PREFASEO

    /home/sromero/plink-1.07-x86_64/plink --noweb \
    --dosage INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large noheader skip0=1 skip1=1 format=3 \
    --fam logHDL_GWAS.fam \
    --map INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map \
    --covar covariables+IMC_GWAS.txt \
    --allow-no-sex \
    --linear \
    --out INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.ASSOC \
    --ci 0.90



#### LDL


##### CHR 1 HASTA CHR 22

##### ANALISIS CON PREFASEO

    /home/sromero/plink-1.07-x86_64/plink --noweb \
    --dosage INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large noheader skip0=1 skip1=1 format=3 \
    --fam logLDL_GWAS.fam \
    --map INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.map \
    --covar covariables+IMC_GWAS.txt \
    --allow-no-sex \
    --linear \
    --out INDIGENAS_GWAS_519_TODASPOB.QC.UNIF_1_imputacion_prephase_large.ASSOC \
    --ci 0.90
