#!/bin/bash

MODEL=$1
TYPE=$2
SEED=$3

declare -a tasks=("assin-ptbr-rte" "assin-ptpt-rte" "assin2-rte" "assin-ptbr-sts" "assin-ptpt-sts" "assin2-sts" "tweetsent")

for TASK in "${tasks[@]}"; do
    bash st-dnn_seed.sh $MODEL $TYPE $TASK $SEED
    rm -rf /root/.cache/torch
done
