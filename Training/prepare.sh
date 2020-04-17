echo "Entering mt-dnn repository"
git clone https://github.com/namisan/mt-dnn
cd mt-dnn
git checkout f444fe9109d

echo "Downloading mt-dnn repository models"
bash download.sh

echo "Getting input data"
cp -v ../move_assin.sh move_assin.sh
mkdir -v data/canonical_data
bash move_assin.sh $1

echo "Patching files"
patch train.py < ../train.patch
patch data_utils/metrics.py < ../metrics.patch

echo "Preparing tasks definitions"
cp -v ../task_defs.sh .
bash task_defs.sh
