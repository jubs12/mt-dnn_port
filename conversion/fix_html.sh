#!/bin/bash

for file in ` find . -name "*.tsv"`
do
    ftfy $file > $file.temp
    mv $file.temp $file
    echo $file
done
