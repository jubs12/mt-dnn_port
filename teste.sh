#!/bin/bash

ARGS="$@"

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")
#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash eval.sh mt-dnn_assin-ptbr+assin2 bert-pt_$TYPE $ARGS
    bash eval.sh mt-dnn_assin2 bert-pt_$TYPE$ARGS
    python eval_assin.py st-dnn assin-1+2 bert-pt_$TYPE $ARGS
    python eval_assin.py st-dnn assin-ptbr+2 bert-pt_$TYPE $ARGS
done

