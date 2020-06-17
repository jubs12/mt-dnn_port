#!/bin/bash

DROPOUT=$1

declare -a tasks=("best-pt" "random-pt" "worst-pt" "assin1-rte")
declare -a seeds=("2016" "2017" "2019" "2020")
declare -a grad_norms=("1.0" "2.0" "5.0")

for GRAD_NORM in "${grad_norms[@]}"; do
	for SEED in "${seeds[@]}"; do
    		for TASK in "${tasks[@]}"; do
        		bash st-dnn_seed_3.sh bert-multilingual base $TASK $SEED $GRAD_NORM $DROPOUT
        		bash st-dnn_seed_3.sh bert-pt base $TASK $SEED $GRAD_NORM $DROPOUT
        		bash st-dnn_seed_3.sh bert-pt large $TASK $SEED $GRAD_NORM $DROPOUT
    		done
	done
done
