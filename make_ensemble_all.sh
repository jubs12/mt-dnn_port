#!/bin/bash

declare -a tasks=("assin-ptbr-rte" "assin-ptpt-rte" "assin2-rte" "assin-ptbr-sts" "assin-ptpt-sts" "assin2-sts" "tweetsent")
declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")


#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        for TASK in "${tasks[@]}"; do
            python ensemble.py "st-dnn"/"$TASK" "$MODEL"_"$TYPE" 
        done
        python ensemble.py mt-dnn_assin "$MODEL"_"$TYPE"
        python ensemble.py mt-dnn_assin+tweetsent "$MODEL"_"$TYPE"
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    python ensemble.py mt-dnn_assin-ptbr+assin2 bert-pt_$TYPE
    python ensemble.py mt-dnn_assin2 bert-pt_$TYPE
    python ensemble.py "st-dnn"/assin-1+2-rte bert-pt_$TYPE
    python ensemble.py "st-dnn"/assin-1+2-sts bert-pt_$TYPE
    python ensemble.py "st-dnn"/assin-ptbr+2-rte bert-pt_$TYPE
    python ensemble.py "st-dnn"/assin-ptbr+2-sts bert-pt_$TYPE
done


#BERT multilingual
for TASK in "${tasks[@]}"; do
    python ensemble.py "st-dnn"/"$TASK" bert-multilingual_base 
done
python ensemble.py mt-dnn_assin bert-multilingual_base
python ensemble.py mt-dnn_assin+tweetsent bert-multilingual_base

python ensemble.py mt-dnn_assin-ptbr+assin2 bert-multilingual_base
python ensemble.py mt-dnn_assin2 bert-multilingual_base

python ensemble.py "st-dnn"/assin-1+2-rte bert-multilingual_base
python ensemble.py "st-dnn"/assin-1+2-sts bert-multilingual_base
python ensemble.py "st-dnn"/assin-ptbr+2-rte bert-multilingual_base
python ensemble.py "st-dnn"/assin-ptbr+2-sts bert-multilingual_base
