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

if test $typo
then
    echo "No option named $typo" >&2
    exit 127
fi

for folder in `find ../assin -maxdepth 1  -name "assin*-*"`
do
    mv ../assin/$folder$original/*.tsv data/canonical_data/
    mv ../assin/$folder/*.yaml ./
    echo "Getting $folder data"
done

if test $tweetsent  
then
    mv ../tweetsent$original/*.tsv data/canonical_data/
    mv ../tweetsent/*.yaml ./
    echo "Getting tweetsent data"
fi
