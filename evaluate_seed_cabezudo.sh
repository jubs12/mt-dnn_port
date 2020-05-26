#!/bin/bash

SEED=$1
DOWNLOAD_FOLDER=$2

declare -a types=("base" "large")

#Cabezudo experiments with bert-pt base
for TYPE in "${types[@]}"; do
    python assin_xml+eval.py st-dnn assin1-rte bert-pt_$TYPE $SEED $DOWNLOAD_FOLDER
    python assin_xml+eval.py st-dnn best-pt bert-pt_$TYPE $SEED $DOWNLOAD_FOLDER
    python assin_xml+eval.py st-dnn random-pt bert-pt_$TYPE $SEED $DOWNLOAD_FOLDER
    python assin_xml+eval.py st-dnn worst-pt bert-pt_$TYPE $SEED $DOWNLOAD_FOLDER
done

python assin_xml+eval.py st-dnn assin1-rte bert-multilingual_base $SEED $DOWNLOAD_FOLDER
python assin_xml+eval.py st-dnn best-pt bert-multilingual_base $SEED $DOWNLOAD_FOLDER
python assin_xml+eval.py st-dnn random-pt bert-multilingual_base $SEED $DOWNLOAD_FOLDER
python assin_xml+eval.py st-dnn worst-pt bert-multilingual_base $SEED $DOWNLOAD_FOLDER