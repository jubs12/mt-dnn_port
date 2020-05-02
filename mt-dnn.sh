#!/bin/bash

MODEL=$1
TYPE=$2

if [ "$3" = "--tweetsent" ]; then
    tweetsent=true
else
    tweetsent=false
fi

cd mt-dnn

echo "Preparing train arguments"
INPUT_EN="../data/input/en"
INPUT_PT="../data/input/pt"

PREPRO_BERT_PT="--model neuralmind/bert-$TYPE-portuguese-cased --root_dir $INPUT_PT"
PREPRO_MULTILINGUAL="--model bert-$TYPE-multilingual-cased --root_dir $INPUT_PT"
PREPRO_BERT=" --model bert-$TYPE-uncased --do_lower_case --root_dir $INPUT_EN"

TRAIN_MT_DNN="--init_checkpoint mt_dnn_models/mt_dnn_$TYPE_uncased.pt \
              --data_dir $INPUT_EN/bert_{$TYPE}_uncased_lower"

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
   echo "running mt-dnn download script ...wait"
   bash download.sh
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

TASK_LIST=assin-ptbr-sts,assin-ptbr-rte,assin-ptpt-sts,assin2-rte,assin-ptpt-rte,assin2-sts
TASK_DEF="--task_def ../data/task-def/assin.yaml"
OUTPUT_FOLDER="mt-dnn_assin"

if [ "$tweetsent" == true ]; then
    TASK_LIST=$TASK_LIST,tweetsent
    TASK_DEF="--task_def ../data/task-def/assin+tweetsent.yaml"
    OUTPUT_FOLDER=$OUTPUT_FOLDER+tweetsent
fi

TASK="--train_datasets $TASK_LIST --test_datasets $TASK_LIST"

python prepro_std.py $PREPRO $TASK_DEF 
python train.py $TRAIN $TASK $TASK_DEF --tensorboard

mkdir output/$OUTPUT_FOLDER/{$MODEL}_{$TYPE}
cp checkpoint/* ../output/$OUTPUT_FOLDER/{$MODEL}_{$TYPE}/
