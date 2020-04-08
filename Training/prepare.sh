#!/bin/bash

tweetsent=false
original=""
typo=false

while test $# -gt 0
do
    case $1 in
        --tweetsent) tweetsent=true        ;;
        --original)  original="original/"  ;;
        *)           typo=$1               ;;
    esac
    
shift;done

if [[ $typo == true ]]
then
    echo "No option named $typo" >&2
    exit 127
fi

git clone https://github.com/namisan/mt-dnn
git checkout 60aa9dc4ec
cd mt-dnn
pip install transformers
bash download.sh
cp ../move_assin.sh move_assin.sh
mkdir data/canonical_data
bash move_assin.sh $tweetsent $original
patch data_utils/metrics.py < ../metrics.patch
patch mt_dnn/model.py < ../model.patch
patch prepro_std.py < ../prepro_std.patch
patch train.py < ../train.patch
cp ../task_defs.sh
bash task_defs.sh
echo "Please copy task_list" 
