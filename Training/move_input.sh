#!/bin/bash

if [[ $1 =~ assin ]];
then
    mv ../assin/$1/*.tsv data/canonical_data/
    mv ../assin/$1/*.yaml ./
else
    mv ../$1/*.tsv data/canonical_data/
    mv ../$1/*.yaml ./
fi
