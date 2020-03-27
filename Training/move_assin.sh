#!/bin/bash

for folder in `find ../assin -maxdepth 1  -name "assin*-*"`
do
    mv ../assin/$folder/*.tsv data/canonical_data/
    mv ../assin/$folder/*.yaml ./
    echo "Getting $folder data"
done

if  [[ $1 = '--tweetsent' ]]
then
    mv ../tweetsent/*.tsv data/canonical_data/
    mv ../tweetsent/*.yaml ./
    echo "Getting tweetsent data"
fi
