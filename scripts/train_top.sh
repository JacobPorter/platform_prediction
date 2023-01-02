#!/bin/bash
# $1 Classifier
nohup srun -A bii_nssac -p bii -n 8 ./simple_estimator.py train -e $1 -f 8 -p 8  /project/biocomplexity/fungcat/jsporter/platform_prediction/models/top_level/$1/ /project/biocomplexity/fungcat/jsporter/platform_prediction/data/train/top_level_3k_header_nosrr_short_features.txt /project/biocomplexity/fungcat/jsporter/platform_prediction/data/train/top_level_3k_header_nosrr_short_labels.txt &> /project/biocomplexity/fungcat/jsporter/platform_prediction/models/top_level/$1/train.$1.out &
