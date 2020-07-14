#!/bin/bash

ARGS="$@"

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")

#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash st-dnn_loop.sh $MODEL $TYPE "$ARGS"
        bash mt-dnn.sh $MODEL $TYPE assin "$ARGS"
        bash mt-dnn.sh $MODEL $TYPE assin+tweetsent "$ARGS"
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash mt-dnn.sh bert-pt $TYPE assin-ptbr+assin2 "$ARGS"
    bash mt-dnn.sh bert-pt $TYPE assin2 "$ARGS"
    for TASK in "${tasks[@]}"; do
        bash st-dnn.sh bert-pt $TYPE assin-1+2-$TASK "$ARGS"
        bash st-dnn.sh bert-pt $TYPE assin-ptbr+2-$TASK "$ARGS"
    done
done

#BERT multilingual
bash st-dnn_loop.sh bert-multilingual base "$ARGS"
bash mt-dnn.sh bert-multilingual base assin "$ARGS"
bash mt-dnn.sh bert-multilingual base assin+tweetsent "$ARGS"

bash mt-dnn.sh bert-multilingual base assin-ptbr+assin2 "$ARGS"
bash mt-dnn.sh bert-multilingual base assin2 "$ARGS"

for TASK in "${tasks[@]}"; do
    bash st-dnn.sh bert-multilingual base assin-1+2-$TASK "$ARGS"
    bash st-dnn.sh bert-multilingual base assin-ptbr+2-$TASK "$ARGS"
done
