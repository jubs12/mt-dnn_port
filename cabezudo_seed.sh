#!/bin/bash

declare -a tasks=("best-pt" "random-pt" "worst-pt" "assin1-rte")
declare -a seeds=("2016" "2017" "2019" "2020")

for SEED in "${seeds[@]}"; do
    for TASK in "${tasks[@]}"; do
        bash st-dnn_seed.sh bert-multilingual base $TASK $SEED
        bash st-dnn_seed.sh bert-pt base $TASK $SEED
        bash st-dnn_seed.sh bert-pt large $TASK $SEED
    done
done
