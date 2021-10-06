#!/bin/sh
# $1 platform
# $2 SRA number
# $3 Amount
nohup srun -A bii_nssac -p bii ./platform_features.py --header /scratch/jsp4cu/platform_prediction/data/$1/$2.$3.fastq $1 1> /scratch/jsp4cu/platform_prediction/data/$1/$2.$3.features 2> /scratch/jsp4cu/platform_prediction/data/$1/$2.$3.extract_features.out &
