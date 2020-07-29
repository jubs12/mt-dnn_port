MODE=$1
MODEL_TYPE=$2
INNER_FOLDER=$3

if [[ "$INNER_FOLDER" != "" ]]; then
   INNER_FOLDER=/$INNER_FOLDER
fi

DOWNLOAD_FOLDER=data/dataset
EVAL_FOLDER=report/$MODE/$MODEL_TYPE$INNER_FOLDER
EVAL_FILE=$EVAL_FOLDER/assin2_hard_label_eval.txt

echo "corpus: assin2 hard label" 
python assin/breakdown-analysis.py $DOWNLOAD_FOLDER/assin2-test.xml $EVAL_FOLDER/assin2-test.xml single-sent.xml
python assin/breakdown-analysis.py $DOWNLOAD_FOLDER/assin2-test.xml $EVAL_FOLDER/assin2-test.xml single-sent.xml > $EVAL_FILE
echo
echo "Saved evaluation: $EVAL_FILE"
echo
echo
