#!/bin/bash

INNER_FOLDER=$1

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")

#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash scripts/eval_hard_label.sh st-dnn "$MODEL"_"$TYPE" $INNER_FOLDER
        bash scripts/eval_hard_label.sh mt-dnn_assin "$MODEL"_"$TYPE" $INNER_FOLDER
        bash scripts/eval_hard_label.sh mt-dnn_assin+tweetsent "$MODEL"_"$TYPE" $INNER_FOLDER
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash scripts/eval_hard_label.sh mt-dnn_assin-ptbr+assin2 bert-pt_$TYPE $INNER_FOLDER
    bash scripts/eval_hard_label.sh mt-dnn_assin2 bert-pt_$TYPE $INNER_FOLDER
    bash scripts/eval_hard_label.sh st-dnn bert-pt_$TYPE $INNER_FOLDER/assin-1+2
    bash scripts/eval_hard_label.sh st-dnn bert-pt_$TYPE $INNER_FOLDER/assin-ptbr+2
done


#BERT multilingual
bash scripts/eval_hard_label.sh st-dnn bert-multilingual_base $INNER_FOLDER
bash scripts/eval_hard_label.sh mt-dnn_assin bert-multilingual_base $INNER_FOLDER
bash scripts/eval_hard_label.sh mt-dnn_assin+tweetsent bert-multilingual_base $INNER_FOLDER

bash scripts/eval_hard_label.sh mt-dnn_assin-ptbr+assin2 bert-multilingual_base $INNER_FOLDER
bash scripts/eval_hard_label.sh mt-dnn_assin2 bert-multilingual_base $INNER_FOLDER


bash scripts/eval_hard_label.sh st-dnn bert-multilingual_base $INNER_FOLDER/assin-1+2
bash scripts/eval_hard_label.sh st-dnn bert-multilingual_base $INNER_FOLDER/assin-ptbr+2
