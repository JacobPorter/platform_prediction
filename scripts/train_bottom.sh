#!/bin/bash
# $1 Classifier
nohup srun -A bii_nssac -p bii  ./simple_estimator.py train -e $1 -p 1  /project/biocomplexity/fungcat/jsporter/platform_prediction/models/bottom_level/mark_2/$1/ /project/biocomplexity/fungcat/jsporter/platform_prediction/data/train/3class.63_files.01012022.shuf.features /project/biocomplexity/fungcat/jsporter/platform_prediction/data/train/3class.63_files.01012022.shuf.labels &> /project/biocomplexity/fungcat/jsporter/platform_prediction/models/bottom_level/mark_2/$1/train.$1.out &
