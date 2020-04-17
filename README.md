# mt-dnn_port
This repository evaluates ST-DNN and MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") on the NLP Portuguese tasks available on [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset") and  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository") datasets.

Most procedures were developed in Google Colaboratory and on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").

This [MTDNN version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") supports Hugging Face Transformers, consequently Portuguese BERT was trained using this branch.
Assin was also executed and there is no difference in performance to master branch.

I was not able to extract embeddings in this [MTDNN version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository").
For that propose please use master branch.

#### ASSIN
 ##### ASSIN ST-DNN
 1. Run Training/train.ipynb for rte and sts

    - mtdnn calculated scores

 2. Get output files from st-dnn model
   ```bash
   cp mt-dnn/checkpoint/{corpus_name}-rte_test_scores_4.json ./results/{corpus_name}-rte_test_scores_4.json
   cp mt-dnn/checkpoint/{corpus_name}-sts_test_scores_4.json ./results/{corpus_name}-sts_test_scores_4.json
   ```
 3. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name} and model = {model_name}
   
    - assin-formated test output files

 4. Run Training/assin/get_benchmarks.ipynb, filling model = {model_name}
   
    - official scores

##### ASSIN MT-DNN
Colab doesn't support ASSIN MT-DNN.

1. Enter MT-DNN container and mt-dnn_port/Training folder
   
   ```bash
   sudo docker pull allenlao/pytorch-mt-dnn:v0.5
   sudo docker run -it  --mount type=bind,source="$(pwd)",target=/container allenlao/pytorch-mt-dnn:v0.5 bash
   cd /container
   
   git clone -b mt-dnn-updated https://github.com/jubs12/mt-dnn_port.git
   cd mt-dnn_port/Training
   bash prepare.sh
   cd mt-dnn/
   ``` 
   - for portuguese dataset, use --original option in prepare.sh
 
2. Train
    - For mt-dnn,
      ```bash
      python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml; \
      python train.py --task_def task_defs.yaml\
      --train_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts \
      --test_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts \
      --tensorboard \
      --data_dir data/canonical_data/bert_base_uncased_lower \
      --init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt
      ```
    - For portuguese bert,
         ```bash
         python prepro_std.py --root_dir data/canonical_data --task_def task_defs.yaml  \
         --model neuralmind/bert-base-portuguese-cased; \
         python train.py --task_def task_defs.yaml \
         --train_datasets assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,assin2-sts,assin2-rte \
         --test_datasets assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,\
         assin2-sts,assin2-rte \
         --data_dir data/canonical_data/bert_base_cased \
         --init_checkpoint neuralmind/bert-base-portuguese-cased
         ```
    - For bert,
       ```bash
      python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml; \
      python train.py --task_def task_defs.yaml \
      --train_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts \
      --test_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts \
      --tensorboard \
      --data_dir data/canonical_data/bert_base_uncased_lower \
      --init_checkpoint bert-base-uncased
      ```
 
3. Get output files from mtdnn model
   ```bash
   cp mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
4. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files

5. Run Training/assin/get_benchmarks.ipynb
   
    - official scores
 
##### TweetSentBR
Tweetsent formatted data is not available due to Twitter Policy.

###### TweetSentBR ST-DNN

 1. Run Training/train.ipynb

    - mtdnn calculated scores
    
 2. Run Training/tweetsent/tweet_result.ipynb
 
    -  test output files

 3. Run Training/tweetsent/get_benchmarks.ipynb
   
    - official scores
    
 ###### ASSIN + TweetSentBR MT-DNN
 Colab doesn't support ASSIN + TweetSentBR MT-DNN.
 1. Enter MT-DNN container and mt-dnn_port/Training folder
   
   ```bash
   sudo docker pull allenlao/pytorch-mt-dnn:v0.5
   sudo docker run -it  --mount type=bind,source="$(pwd)",target=/container allenlao/pytorch-mt-dnn:v0.5 bash
   cd /container
   git clone -b mt-dnn-updated https://github.com/jubs12/mt-dnn_port.git
   bash prepare.sh
   ``` 
   - for portuguese dataset, use --original option in prepare.sh
  
2. Train
    - For mt-dnn,
      ```bash
      python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml; \
      python train.py --task_def task_defs.yaml\
      --train_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,tweetsent \
      --test_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,tweetsent \
      --tensorboard \
      --data_dir data/canonical_data/bert_base_uncased_lower \
      --init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt
      ```
    - For portuguese bert,
         ```bash
         python prepro_std.py --root_dir data/canonical_data --task_def task_defs.yaml  \
         --model neuralmind/bert-base-portuguese-cased; \
         python train.py --task_def task_defs.yaml \
         --train_datasets assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,assin2-sts,assin2-rte,tweetsent \
         --test_datasets assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,assin2-sts,assin2-rte,tweetsent\
         --data_dir data/canonical_data/bert_base_cased \
         --init_checkpoint neuralmind/bert-base-portuguese-cased
         ```
    - For bert,
       ```bash
      python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml; \
      python train.py --task_def task_defs.yaml \
      --train_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,tweetsent \
      --test_datasets assin2-sts,assin2-rte,assin-ptbr-rte,assin-ptpt-rte,assin-ptpt-sts,assin-ptbr-sts,tweetsent \
      --tensorboard \
      --data_dir data/canonical_data/bert_base_uncased_lower \
      --init_checkpoint bert-base-uncased
      ```
      ```
 
3. Get output files from mtdnn model
   ```bash
   cp mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
4. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files
5. Run Training/assin/get_benchmarks.ipynb
   
    - official scores
    
6. Run Training/tweetsent/tweet_result.ipynb
 
    -  test output files

7. Run Training/tweetsent/get_benchmarks.ipynb
   
    - official scores
