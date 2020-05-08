#!/bin/bash

MODE=$1
PRETRAINED=$2

declare -a assin=("assin-ptbr" "assin-ptpt" "assin2")
declare -a assin_ptbr_2=("assin-ptbr" "assin2")
declare -a assin2=("assin2")

if [ "$MODE" = "mt-dnn_assin" ]; then
    DATASETS=("${assin[@]}")
elif [ "$MODE" = "mt-dnn_assin-ptbr+assin2" ]; then
    DATASETS=("${assin_ptbr_2[@]}")
elif [ "$MODE" = "mt-dnn_assin2" ]; then
    DATASETS=("${assin_2[@]}")
elif [ "$MODE" = "st-dnn" ]; then
    DATASETS=("${assin[@]}")
else
   echo "invalid $MODE option">&2
   exit 127
fi

for DATASET in "${DATASETS[@]}"; do
    python assin_xml+eval.py $MODE $DATASET $PRETRAINED
done