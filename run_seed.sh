#!/bin/bash

SEED=$1

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")


#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash st-dnn_loop_seed.sh $MODEL $TYPE $SEED
        bash mt-dnn_seed.sh $MODEL $TYPE assin $SEED
        bash mt-dnn_seed.sh $MODEL $TYPE assin+tweetsent $SEED
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash mt-dnn_seed.sh bert-pt $TYPE assin-ptbr+assin2 $SEED
    bash mt-dnn_seed.sh bert-pt $TYPE assin2 $SEED
    for TASK in "${tasks[@]}"; do
        bash st-dnn_seed.sh bert-pt $TYPE assin-1+2-$TASK $SEED
        bash st-dnn_seed.sh bert-pt $TYPE assin-ptbr+2-$TASK $SEED
    done
done


#BERT multilingual
bash st-dnn_loop_seed.sh bert-multilingual base $SEED
bash mt-dnn_seed.sh bert-multilingual base assin $SEED
bash mt-dnn_seed.sh bert-multilingual base assin+tweetsent $SEED

bash mt-dnn_seed.sh bert-multilingual base assin-ptbr+assin2 $SEED
bash mt-dnn_seed.sh bert-multilingual base assin2 $SEED

for TASK in "${tasks[@]}"; do
    bash st-dnn_seed.sh bert-multilingual base assin-1+2-$TASK $SEED
    bash st-dnn_seed.sh bert-multilingual base assin-ptbr+2-$TASK $SEED
done
