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

echo "Entering mt-dnn repository"
git clone https://github.com/namisan/mt-dnn
git checkout 60aa9dc4ec
cd mt-dnn

echo "Installing transformers"
pip install transformers

echo "Download mt-dnn repository models: [y/n]"
echo "For bert and Portuguese bert, select n"
echo "For mt-dnn, select y"
read download

if ["$download" = "y" ]; then
    bash download.sh
fi


echo "Getting input data"
cp ../move_assin.sh move_assin.sh
mkdir data data/canonical_data
bash move_assin.sh $tweetsent $original

echo "Patching files"
patch data_utils/metrics.py < ../metrics.patch
patch mt_dnn/model.py < ../model.patch
patch prepro_std.py < ../prepro_std.patch
patch train.py < ../train.patch

echo "Preparing tasks definitions"
cp ../task_defs.sh
bash task_defs.sh
echo "Please copy task_list" 
echo "Also note the current work directory is $pwd"
