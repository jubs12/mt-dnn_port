#!/bin/bash

if [[ $1 =~ assin ]];
then
    mv mtdnn_port/Training/assin/$1/*.tsv data/canonical_data/
    mv mtdnn_port/Training/assin/$1/*.yaml ./
else
    mv mtdnn_port/Training/$1/*.tsv data/canonical_data/
    mv mtdnn_port/Training/$1/*.yaml ./
fi
