#!/bin/bash

MODEL=$1
TYPE=$2
TASK=$3
SEED=$4

cd mt-dnn

echo "Preparing train arguments"
INPUT_EN="../data/input/en"
INPUT_PT="../data/input/pt"

PREPRO_BERT_PT="--model neuralmind/bert-$TYPE-portuguese-cased --root_dir $INPUT_PT"
PREPRO_MULTILINGUAL="--model bert-$TYPE-multilingual-cased --root_dir $INPUT_PT"
PREPRO_BERT=" --model bert-$TYPE-uncased --do_lower_case --root_dir $INPUT_EN"

TRAIN_MT_DNN="--init_checkpoint mt_dnn_models/mt_dnn_${TYPE}_uncased.pt \
              --data_dir $INPUT_EN/bert_${TYPE}_uncased_lower"

TRAIN_BERT="--init_checkpoint bert-$TYPE-uncased \
            --data_dir $INPUT_EN/bert_${TYPE}_uncased_lower"

TRAIN_MULTILINGUAL="--data_dir $INPUT_PT/bert_${TYPE}_cased \
                  --init_checkpoint bert-$TYPE-multilingual-cased"

TRAIN_BERT_PT="--data_dir $INPUT_PT/bert_${TYPE}_cased \
               --init_checkpoint neuralmind/bert-$TYPE-portuguese-cased"

if [ "$MODEL" = "bert" ]; then
   PREPRO=$PREPRO_BERT
   TRAIN=$TRAIN_BERT
elif [ "$MODEL" =  "mt-dnn" ]; then
   if [ ! -f "mt_dnn_models/mt_dnn_${TYPE}_uncased.pt" ]; then
      echo "running mt-dnn download script ...wait"
      bash download.sh
   fi
   PREPRO=$PREPRO_BERT
   TRAIN=$TRAIN_MT_DNN
elif [ "$MODEL" = "bert-pt" ]; then
   PREPRO=$PREPRO_BERT_PT
   TRAIN=$TRAIN_BERT_PT
elif [ "$MODEL" = "bert-multilingual" ]; then
   PREPRO=$PREPRO_MULTILINGUAL
   TRAIN=$TRAIN_MULTILINGUAL
else
   echo "invalid option">&2
   exit 127
fi

declare -a tasks_cabezudo=("assin1-rte" "best-pt" "worst-pt" "random-pt")
if [[ " ${tasks_cabezudo[@]} " =~ " ${TASK} " ]]; then
        CABEZUDO="--epochs 7 --learning_rate 0.00002 --batch_size 22 --batch_size_eval 22 --max_seq_len 128"
fi

python prepro_std.py --task_def ../data/task-def/$TASK.yaml $PREPRO
python train.py $CABEZUDO  --task_def ../data/task-def/$TASK.yaml --train_datasets $TASK --test_datasets $TASK --tensorboard $TRAIN --output_dir ../output/st-dnn/$TASK/${MODEL}_${TYPE}/seed/$SEED --seed $SEED --fp16
rm -rf ../output/st-dnn/$TASK/${MODEL}_${TYPE}/seed/$SEED/model_*.pt
