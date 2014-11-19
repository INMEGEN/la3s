# Local Ancestry Adjustment for Association Study

Asociación de polimorfismos a rasgos metabólicos utilizando
microarreglos de genotipificación ajustando por ancestría local.


***

## Insumos

### infile
Archivos por población con los 442,450 SNPs, ''infile''

    INDIGENAS_GWAS_519_NAHUAS.QC.UNIF.bed , *.bim, *.fam
    INDIGENAS_GWAS_519_MAYAS.QC.UNIF, *.bim, *.fam
    INDIGENAS_GWAS_519_TOTONACOS.QC.UNIF, *.bim, *.fam
    INDIGENAS_GWAS_519_ZAPOTECOS.QC.UNIF, *.bim, *.fam

### frq file

    INDIGENAS_GWAS_519_TODASPOB.QC.UNIF.frq

### phenofile

    nahuas_logLDL_EMMAX.txt
    mayas_logLDL_EMMAX.txt
    totonacos_logLDL_EMMAX.txt
    zapotecos_logLDL_EMMAX.txt

### kifile

    INDIGENAS_GWAS_519_NAHUAS.QC.UNIF.EMMAX.tr.aIBS.kinf
    INDIGENAS_GWAS_519_MAYAS.QC.UNIF.EMMAX.tr.aIBS.kinf
    INDIGENAS_GWAS_519_TOTONACOS.QC.UNIF.EMMAX.tr.aIBS.kinf
    INDIGENAS_GWAS_519_ZAPOTECOS.QC.UNIF.EMMAX.tr.aIBS.kinf

### covariate templates

    covariables_NAHUAS+IMC_EMMAX_AUTO.txt
    covariables_MAYAS+IMC_EMMAX_AUTO.txt
    covariables_TOTONACOS+IMC_EMMAX_AUTO.txt
    covariables_ZAPOTECOS+IMC_EMMAX_AUTO.txt




***



## Pipeline

### 1. Extraer los snps que están dentro de cada segmento. 


Esto se puede hacer con PLINK utilizando alguno de los siguiente comandos:

    plink --bfile infile --chr 2 --from-kb 5000 --to-kb 10000 --make-bed --out outfile.1

### 2. Transponer los archivos obtenidos en el paso anterior 1)


Esto se puede hacer también con plink usando el siguiente comando: 

    plink --bfile outfile.1 --recode12 --output-missing-genotype 0 --transpose --out outfile.2

### 3. Construir el archivo de covariables


En este paso, tenemos que integrar la covariable del segmento al
archivo original de covariables, que incluye IMC, edad y genero.

### 4. Correr el análisis de asociación segmento x segmento, población x población, con el programa EMMAX


Los archivos requeridos para correr EMMAX son:

1. archivo transpuesto (paso 2: outfile.2)
2. archivo de fenotipos (fijo: phenfile)
3. archivo de covariables (covfile.3)
4. archivo kinship matrix (fijo: kinfile)

El comando para correr EMMAX es el siguiente:

    emmax-intel64 -v -d 10 -t outfile.2  -p phenfile -c covfile.3 -k kinfile -o outfile.4

Este paso se corre para cada una de las poblaciones por separado:
nahuas, mayas, zapotecos y totonacos, por lo que tenemos 4 archivos de
salida con formato .ps

    outfile.4.nah
    outfile.4.may
    outfile.4.zap
    outfile.4.tot

### 5. Formatear los archivos de salida de EMMAX para que puedan entrar a METAL

Este último va a combinar los resultados de las 4 poblaciones.

#### 5.1) Mover los archivos .ps a .txt

    mv outfile.4.nah.ps outfile.4.nah.txt

#### 5.2) Ponerle título

    echo "SNP BETA SE P" > header.txt
    cat header.txt outfile.4.nah.txt > tmp1
    mv tmp1 outfile.4.nah.1.txt

#### 5.3) Agregarle al archivo la frecuencia del alelo. Contamos ya con el archivo frq

    join -1 2 -2 1 allpopulation.frq outfile.4.nah.1.txt > outfile.4.nah.det.txt

#### 5.4) Obtener los rs´s y posición del archivo .bim para después fusionar los archivos

    echo "SNP BP" > chr.txt
    awk '{print  $2, $4}' infile.bim >> chr.txt
    join -1 1 -2 1 chr.txt outfile.4.nah.det.txt > tmp1
    mv tmp1 outfile.4.nah.detail.txt 



### 6. Correr METAL

Se utiliza un archivo como el siguiente, nombrado para fines de
ejemplo README_METAL_logLDL:

    SCHEME   STDERR
    STDERR SE
    GENOMICCONTROL ON
    AVERAGEFREQ ON
    MINMAXFREQ ON
    MARKER SNP
    ALLELE A1 A2
    FREQLABEL MAF
    EFFECT BETA
    STDERR   SE
    PVAL     P
    PROCESS outfile.4.nah.detail.txt
    MARKER SNP
    ALLELE A1 A2
    FREQLABEL MAF
    EFFECT BETA
    STDERR   SE
    PVAL     P
    PROCESS outfile.4.may.detail.txt
    MARKER SNP
    ALLELE A1 A2
    FREQLABEL MAF
    EFFECT BETA
    STDERR   SE
    PVAL     P
    PROCESS outfile.4.tot.detail.txt 
    MARKER SNP
    ALLELE A1 A2
    FREQLABEL MAF
    EFFECT BETA
    STDERR   SE
    PVAL     P
    PROCESS outfile.4.zap.detail.txt 
    OUTFILE metal_outfile.tbl
    ANALYZE
    QUIT

metal README_METAL_logLDL

El archivo de salida es METAANALYSIS1.TBL, por lo que se recomienda
cambiarle el nombre y moverlo de carpeta

    mv METAANALYSIS1.TBL metal_outfile.tbl

### 7. Continuar con el siguiente segmento




## Dependencies

- [plink](http://pngu.mgh.harvard.edu/~purcell/plink/)
- [EMMAX](http://www.sph.umich.edu/csg/kang/emmax/download/index.html)
- [METAL](http://www.sph.umich.edu/csg/abecasis/metal/)
