#!/bin/bash

ARGS="$@"
declare -a tasks=("best-pt" "random-pt" "worst-pt" "assin1-rte")

for TASK in "${tasks[@]}"; do
	bash scripts/st-dnn.sh bert-multilingual base $TASK "$ARGS"
	bash scripts/st-dnn.sh bert-pt base $TASK "$ARGS"
	bash scripts/st-dnn.sh bert-pt large $TASK "$ARGS"
done
