#!/bin/bash

declare -a tasks=("assin-ptbr-rte" "assin-ptpt-rte" "assin2-rte" "assin-ptbr-sts" "assin-ptpt-sts" "assin2-sts", "tweetsent")

for TASK in "${tasks[@]}"; do
    echo bash st-dnn.sh bert-multilingual base $TASK
done
