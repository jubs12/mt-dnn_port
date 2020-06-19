#!/bin/bash

declare -a models=("bert-multilingual_base" "bert-pt_base" "bert-pt_large")

for MODEL in "${models[@]}"; do
    python ensemble.py "st-dnn"/assin1-rte $MODEL 
    python ensemble.py "st-dnn"/best-pt $MODEL
    python ensemble.py "st-dnn"/random-pt $MODEL
    python ensemble.py "st-dnn"/worst-pt $MODEL

done


