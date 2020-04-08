git clone https://github.com/namisan/mt-dnn
git checkout f444fe9109d
cd mt-dnn
bash download.sh
cp ../move_assin.sh move_assin.sh
mkdir data/canonical_data
bash move_assin.sh $1
patch train.py < ../train.patch
patch data_utils/metrics.py < ../metrics.patch
cp ../task_defs.sh
bash task_defs.sh
echo "Please copy task_list" 
