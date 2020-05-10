#!/bin/bash

download_folder=data/dataset
mkdir $download_folder

pip install xmltodict
pip install gdown

echo Downloading ASSIN raw dataset in $download_folder

gdown --id 1jkk-0YM2S8MEezIbjduptU6tMXgHzPOs -O $download_folder/assin2-blind-test.xml
gdown --id 1J3FpQaHxpM-FDfBUyooh-sZF-B-bM_lU -O $download_folder/assin2-test.xml
wget http://nilc.icmc.usp.br/assin/assin.tar.gz
tar -xzf assin.tar.gz  -C $download_folder/
rm -rf assin.tar.gz

#ASSIN official evaluation
git clone https://github.com/erickrf/assin.git

echo Extracting tweetSentBR raw dataset in $download_folder
if test -f tweetSentBR_extracted.zip; then
    mv tweetSentBR_extracted.zip $download_folder
    unzip $download_folder/tweetSentBR_extracted.zip -d $download_folder
else
    echo 'To evaluate tweetSentBR dataset please provide tweetSentBR_extracted.zip'
fi

#TweetsentBR official evaluation
git clone https://bitbucket.org/HBrum/tweetsentbr.git
touch tweetsentbr/__init__.py 
touch tweetsentbr/sent-analysis/__init__.py 

pip install nlpnet
