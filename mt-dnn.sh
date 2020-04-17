#!/bin/bash

MODEL=$1

if [ "$2" = "--tweetsent" ]; then
    tweetsent=true
else
    tweetsent=false
fi

echo "Entering mt-dnn repository"
git clone https://github.com/namisan/mt-dnn
cd mt-dnn
git checkout 60aa9dc4ec

echo "Installing transformers"
pip install transformers

echo "Patching files"
patch data_utils/metrics.py < "../utils/patch/metrics.patch"
patch mt_dnn/model.py < "../utils/patch/model.patch"
patch prepro_std.py < "../utils/patch/prepro_std.patch"
patch train.py < "../utils/patch/train.patch"

echo "Preparing train arguments"
INPUT_EN="../data/input/en"
INPUT_PT="../data/input/pt"

PREPRO_BERT_PT="--model neuralmind/bert-base-portuguese-cased --root_dir $INPUT_PT"
PREPRO_BERT="--do_lower_case --root_dir $INPUT_EN"

TRAIN_MT_DNN="--init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt \
              --data_dir $INPUT_EN/bert_base_uncased_lower"

TRAIN_BERT="--init_checkpoint bert-base-uncased \
            --data_dir $INPUT_EN/bert_base_uncased_lower"

TRAIN_BERT_PT="--data_dir $INPUT_PT/bert_base_cased \
               --init_checkpoint neuralmind/bert-base-portuguese-cased"

if [ "$MODEL" = "bert" ]; then
   PREPRO=PREPRO_BERT
   TRAIN=TRAIN_BERT
elif [ "$MODEL" =  "mt-dnn" ]; then
   echo "running mt-dnn download script ...wait"
   !bash download.sh
   PREPRO=PREPRO_BERT
   TRAIN=TRAIN_MT_DNN
elif [ "$MODEL" = "bert-pt" ]; then
   PREPRO=PREPRO_BERT_PT
   TRAIN=TRAIN_BERT_PT
else
   echo "invalid option">&2
   exit 127
fi

TASK_LIST=assin-ptbr-sts,assin-ptbr-rte,assin-ptpt-sts,assin2-rte,assin-ptpt-rte,assin2-sts
TASK_DEF="--task_def ../data/task-def/assin.yaml"

if [ "$tweetsent" == true ]; then
    TASK_LIST=$TASK_LIST,tweetsent
    TASK_DEF="--task_def ../data/task-def/assin+tweetsent.yaml"
fi

TASK="--train_datasets $TASK_LIST --test_datasets $TASK_LIST"

python prepro_std.py "$PREPRO" "$TASK_DEF" 
python train.py "$TRAIN" "$TASK" "$TASK_DEF" --tensorboard
