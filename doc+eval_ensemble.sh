#!/bin/bash

MODE=$1
PRETRAINED=$2
DOWNLOAD_FOLDER=$3

declare -a assin=("assin-ptbr" "assin-ptpt" "assin2")
declare -a assin_ptbr_2=("assin-ptbr" "assin2")
declare -a assin2=("assin2")

if [ "$MODE" = "mt-dnn_assin+tweetsent" ]; then
    DATASETS=("${assin[@]}")
elif [ "$MODE" = "mt-dnn_assin" ]; then
    DATASETS=("${assin[@]}")
elif [ "$MODE" = "mt-dnn_assin-ptbr+assin2" ]; then
    DATASETS=("${assin_ptbr_2[@]}")
elif [ "$MODE" = "mt-dnn_assin2" ]; then
    DATASETS=("${assin2[@]}")
elif [ "$MODE" = "st-dnn" ]; then
    DATASETS=("${assin[@]}")
else
   echo "invalid $MODE option">&2
   exit 127
fi

for DATASET in "${DATASETS[@]}"; do
    python assin_xml+eval_ensemble.py $MODE $DATASET $PRETRAINED $DOWNLOAD_FOLDER
done

tweetsent_modes=("st-dnn" "mt-dnn_assin+tweetsent")

if [[ " ${tweetsent_modes[@]} " =~ " ${MODE} " ]]; then
    python tweetsent_json+eval_ensemble.py $MODE $PRETRAINED $DOWNLOAD_FOLDER
fi


