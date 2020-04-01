#!/bin/bash

for task in `find . -maxdepth 1  -name "*.yaml"`
do
    python prepro_std.py --root_dir data/canonical_data "$*"
fi
done
