echo "Entering mt-dnn repository"
git clone https://github.com/namisan/mt-dnn
cd mt-dnn
git checkout 60aa9dc4ec

echo "Installing transformers"
pip install transformers

echo "Patching files"
patch data_utils/metrics.py < "../utils/patch/metrics.patch"
patch mt_dnn/model.py < "../utils/patch/model.patch"
patch prepro_std.py < "../utils/patch/prepro_std.patch"
patch train.py < "../utils/patch/train.patch"
