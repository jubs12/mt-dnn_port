#!/bin/bash

for task in `find . -maxdepth 1  -name "*.yaml"`
do
if  [[ $1 = '--do_lower_case' ]]
then
    python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def ${task%.yaml}.yaml
else
    python prepro_std.py --root_dir data/canonical_data --task_def ${task%.yaml}.yaml
fi
done
