#!/bin/bash

SEED=$1
GRAD_NORM=$2
DROPOUT=$3

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")


#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash st-dnn_loop_seed_3.sh $MODEL $TYPE $SEED $GRAD_NORM $DROPOUT
        bash mt-dnn_seed_3.sh $MODEL $TYPE assin $SEED $GRAD_NORM $DROPOUT
        bash mt-dnn_seed_3.sh $MODEL $TYPE assin+tweetsent $SEED $GRAD_NORM $DROPOUT
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash mt-dnn_seed_3.sh bert-pt $TYPE assin-ptbr+assin2 $SEED $GRAD_NORM $DROPOUT
    bash mt-dnn_seed_3.sh bert-pt $TYPE assin2 $SEED $GRAD_NORM $DROPOUT
    for TASK in "${tasks[@]}"; do
        bash st-dnn_seed_3.sh bert-pt $TYPE assin-1+2-$TASK $SEED $GRAD_NORM $DROPOUT
        bash st-dnn_seed_3.sh bert-pt $TYPE assin-ptbr+2-$TASK $SEED $GRAD_NORM $DROPOUT
    done
done


#BERT multilingual
bash st-dnn_loop_seed_3.sh bert-multilingual base $SEED $GRAD_NORM $DROPOUT
bash mt-dnn_seed_3.sh bert-multilingual base assin $SEED $GRAD_NORM $DROPOUT
bash mt-dnn_seed_3.sh bert-multilingual base assin+tweetsent $SEED $GRAD_NORM $DROPOUT

bash mt-dnn_seed_3.sh bert-multilingual base assin-ptbr+assin2 $SEED $GRAD_NORM $DROPOUT
bash mt-dnn_seed_3.sh bert-multilingual base assin2 $SEED $GRAD_NORM $DROPOUT

for TASK in "${tasks[@]}"; do
    bash st-dnn_seed_3.sh bert-multilingual base assin-1+2-$TASK $SEED $GRAD_NORM $DROPOUT
    bash st-dnn_seed_3.sh bert-multilingual base assin-ptbr+2-$TASK $SEED $GRAD_NORM $DROPOUT
done
