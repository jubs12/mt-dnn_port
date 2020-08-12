#!/bin/bash

declare -a grad_norms=("1.0" "2.0" "5.0")
declare -a dropouts=("0.1" "0.05" "0.3")

for GRAD_NORM in "${grad_norms[@]}"; do
    for DROPOUT in "${dropouts[@]}"; do
        echo $SEED $GRAD_NORM $DROPOUT
        python mean.py $GRAD_NORM $DROPOUT
    done
done
