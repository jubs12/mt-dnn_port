#!/bin/bash

GRAD_NORM=$1

declare -a tasks=("best-pt" "random-pt" "worst-pt" "assin1-rte")
declare -a seeds=("2016" "2017" "2018" "2019" "2020")

for SEED in "${seeds[@]}"; do
    for TASK in "${tasks[@]}"; do
        bash st-dnn_seed_2.sh bert-multilingual base $TASK $SEED $GRAD_NORM
        bash st-dnn_seed_2.sh bert-pt base $TASK $SEED $GRAD_NORM
        bash st-dnn_seed_2.sh bert-pt large $TASK $SEED $GRAD_NORM
    done
done
