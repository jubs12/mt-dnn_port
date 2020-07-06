#!/bin/bash

ARGS="$@"

declare -a models=("bert" "mt-dnn" "bert-pt")
declare -a types=("base" "large")
declare -a tasks=("rte" "sts")


#Initial experiments
for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        bash eval.sh st-dnn "$MODEL"_"$TYPE" $ARGS
        bash eval.sh mt-dnn_assin "$MODEL"_"$TYPE" $ARGS
        bash eval.sh mt-dnn_assin+tweetsent "$MODEL"_"$TYPE" $ARGS
    done
done

#IPR experiments w/ bert base
for TYPE in "${types[@]}"; do
    bash eval.sh mt-dnn_assin-ptbr+assin2 bert-pt_$TYPE $ARGS
    bash eval.sh mt-dnn_assin2 bert-pt_$TYPE $ARGS
    python eval_assin.py st-dnn assin-1+2 bert-pt_$TYPE $ARGS
    python eval_assin.py st-dnn assin-ptbr+2 bert-pt_$TYPE $ARGS
done


#BERT multilingual
bash eval.sh st-dnn bert-multilingual_base $ARGS
bash eval.sh mt-dnn_assin bert-multilingual_base $ARGS
bash eval.sh mt-dnn_assin+tweetsent bert-multilingual_base $ARGS

bash eval.sh mt-dnn_assin-ptbr+assin2 bert-multilingual_base $ARGS
bash eval.sh mt-dnn_assin2 bert-multilingual_base $ARGS


python eval_assin.py st-dnn assin-1+2 bert-multilingual_base $ARGS
python eval_assin.py st-dnn assin-ptbr+2 bert-multilingual_base $ARGS

#Cabezudo experiments
for TYPE in "${types[@]}"; do
    python eval_assin.py st-dnn assin1-rte bert-pt_"$TYPE" $ARGS
    python eval_assin.py st-dnn best-pt bert-pt_"$TYPE" $ARGS
    python eval_assin.py st-dnn random-pt bert-pt_"$TYPE" $ARGS
    python eval_assin.py st-dnn worst-pt bert-pt_"$TYPE" $ARGS
done

python eval_assin.py st-dnn assin1-rte bert-multilingual_base $ARGS
python eval_assin.py st-dnn best-pt bert-multilingual_base $ARGS
python eval_assin.py st-dnn random-pt bert-multilingual_base $ARGS
python eval_assin.py st-dnn worst-pt bert-multilingual_base $ARGS

