#!/bin/bash

MODEL=$1
TYPE=$2
SEED_OR_MODE=$3
GRAD_NORM=$4
DROPOUT=$5

declare -a tasks=("assin-ptbr-rte" "assin-ptpt-rte" "assin2-rte" "assin-ptbr-sts" "assin-ptpt-sts" "assin2-sts" "tweetsent")

for TASK in "${tasks[@]}"; do
    bash st-dnn.sh $MODEL $TYPE $TASK $SEED_OR_MODE $GRAD_NORM $DROPOUT
done
