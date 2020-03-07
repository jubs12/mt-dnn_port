#!/bin/bash

if [[ $1 =~ assin ]];
then
    mv ../Training/assin/$1/*.tsv data/canonical_data/
    mv ../Training/assin/$1/*.yaml ./
else
    mv ../Training/$1/*.tsv data/canonical_data/
    mv ../Training/$1/*.yaml ./
fi
