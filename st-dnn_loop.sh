#!/bin/bash

MODEL=$1
TYPE=$2

declare -a tasks=("assin-ptbr-rte" "assin-ptpt-rte" "assin2-rte" "assin-ptbr-sts" "assin-ptpt-sts" "assin2-sts" "tweetsent")

for TASK in "${tasks[@]}"; do
    bash st-dnn.sh $MODEL $TYPE $TASK
    #rm -rf /root/.cache/torch
done
