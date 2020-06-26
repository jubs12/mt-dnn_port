#!/bin/bash

DOWNLOAD_FOLDER=$1

declare -a types=("base" "large")

#Cabezudo experiments with bert-pt base
for TYPE in "${types[@]}"; do
    python assin_xml+eval_ensemble.py st-dnn assin1-rte bert-pt_$TYPE $DOWNLOAD_FOLDER
    python assin_xml+eval_ensemble.py st-dnn best-pt bert-pt_$TYPE $DOWNLOAD_FOLDER
    python assin_xml+eval_ensemble.py st-dnn random-pt bert-pt_$TYPE $DOWNLOAD_FOLDER
    python assin_xml+eval_ensemble.py st-dnn worst-pt bert-pt_$TYPE $DOWNLOAD_FOLDER
done

python assin_xml+eval_ensemble.py st-dnn assin1-rte bert-multilingual_base $DOWNLOAD_FOLDER
python assin_xml+eval_ensemble.py st-dnn best-pt bert-multilingual_base $DOWNLOAD_FOLDER
python assin_xml+eval_ensemble.py st-dnn random-pt bert-multilingual_base $DOWNLOAD_FOLDER
python assin_xml+eval_ensemble.py st-dnn worst-pt bert-multilingual_base $DOWNLOAD_FOLDER
