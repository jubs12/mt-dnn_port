echo "Normally, the model is downloaded on the 3rd attempt"

attempt=1

while `find . -name 'mt_dnn_models' -type d` == ""
do
   echo "Attempt $attempt"
   bash download.sh
   attempt=$(( $attempt + 1 ))
done
