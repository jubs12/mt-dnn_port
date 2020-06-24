#!/bin/bash

DOWNLOAD_FOLDER=$1

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")


#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash doc+eval_ensemble.sh st-dnn "$MODEL"_"$TYPE" $DOWNLOAD_FOLDER
        bash doc+eval_ensemble.sh mt-dnn_assin "$MODEL"_"$TYPE" $DOWNLOAD_FOLDER
        bash doc+eval_ensemble.sh mt-dnn_assin+tweetsent "$MODEL"_"$TYPE" $DOWNLOAD_FOLDER
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash doc+eval_ensemble.sh mt-dnn_assin-ptbr+assin2 bert-pt_$TYPE$DOWNLOAD_FOLDER
    bash doc+eval_ensemble.sh mt-dnn_assin2 bert-pt_$TYPE$DOWNLOAD_FOLDER
    python assin_xml+eval_ensemble.py st-dnn assin-1+2 bert-pt_$TYPE$DOWNLOAD_FOLDER
    python assin_xml+eval_ensemble.py st-dnn assin-ptbr+2 bert-pt_$TYPE$DOWNLOAD_FOLDER
done


#BERT multilingual
bash doc+eval_ensemble.sh st-dnn bert-multilingual_base$DOWNLOAD_FOLDER
bash doc+eval_ensemble.sh mt-dnn_assin bert-multilingual_base$DOWNLOAD_FOLDER
bash doc+eval_ensemble.sh mt-dnn_assin+tweetsent bert-multilingual_base$DOWNLOAD_FOLDER

bash doc+eval_ensemble.sh mt-dnn_assin-ptbr+assin2 bert-multilingual_base$DOWNLOAD_FOLDER
bash doc+eval_ensemble.sh mt-dnn_assin2 bert-multilingual_base$DOWNLOAD_FOLDER


python assin_xml+eval_ensemble.py st-dnn assin-1+2 bert-multilingual_base$DOWNLOAD_FOLDER
python assin_xml+eval_ensemble.py st-dnn assin-ptbr+2 bert-multilingual_base$DOWNLOAD_FOLDER

