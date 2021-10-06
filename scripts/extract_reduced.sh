#!/bin/sh
# $1 platform
# $2 SRA number
# $3 Amount
# $4 type: train, test
nohup srun -A bii_nssac -p bii ./platform_features.py --reduced /scratch/jsp4cu/platform_prediction/data/$4/$1/$2.$3.fastq $1 1> /scratch/jsp4cu/platform_prediction/data/$4/$1/$2.$3.reduced.features 2> /scratch/jsp4cu/platform_prediction/data/$4/$1/$2.$3.extract_reduced_features.out &
