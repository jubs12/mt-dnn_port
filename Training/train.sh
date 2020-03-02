python train.py \
--do_lower_case \
--log_file $1.log \
--init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt \
--task_def $1.yaml \
--train_datasets $1 \
--test_datasets $1_train,$1_dev,$1_test \
--train_datasets $1
