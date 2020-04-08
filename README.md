# mt-dnn_port
This repository evaluates ST-DNN and MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository") on the NLP Portuguese tasks available on the following datasets: [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset"),  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository"),  [B2W-Reviews01](https://github.com/b2wdigital/b2w-reviews01 "B2W repository") , and [FaQuAD](https://github.com/liafacom/faquad "faquad repository").

Most procedures were developed in Google Colaboratory. 

B2W review_title embedding was extracted on Google Cloud VM: n1-standard-8 (8 CPU, memory 30 GB) Ubuntu 16.04 using Anaconda.

The code was also tested on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").

*For Portuguese BERT related code, please access mt-dnn-updated branch.*

## Translation

The input is translated to English to feed MT-DNN, using the Google Cloud API.

The translation process is shown in Jupyter notebooks for each task.

## Embeddings

Extractor embedding is applied to raw datasets: b2w and faquad (dataset.json).

Files faquad_txt.ipynb and b2w_txt.ipynb convert raw dataset in input for embedding extractor.
However, input data are provided in folders.


#### FaQuad

 Run Embedding/faquad/faquad_embedding.ipynb

#### B2W
Colab doesn't support B2W extractor embbedings.

1. Install requirements for mt-dnn
   
   ```bash
   bash requirements.sh
   ```

2. Move input embeddings for B2W to mt-dnn folder


   ```bash
   cp Embeddings/b2w mt-dnn/b2w
   ```

3. Enter folder  
   ```bash
   cd b2w
   ```

4. Run extractor

   ```bash
   python extractor.py --do_lower_case --finput b2w/review_title.txt --foutput b2w/review_title.json --bert_model bert-base-uncased --checkpoint mt_dnn_models/mt_dnn_base_uncased.pt
   ```

### Training
For all tasks run train.ipynb to get output files.

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
For more flexible version, see readme in mt-dnn-updated branch.

1. Enter MT-DNN container and mt-dnn_port/Training folder
   
   ```bash
   sudo docker pull allenlao/pytorch-mt-dnn:v0.5
   sudo docker run -it  --mount type=bind,source="$(pwd)",target=/container allenlao/pytorch-mt-dnn:v0.5 bash
   cd /container
   git clone https://github.com/jubs12/mt-dnn_port.git
   cd mt-dnn_port/Training
   bash prepare.sh
   ```
   
2. Preprocess Data
 ```bash
   python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml
 ```
 
3. Train task

```bash
  python train.py  --init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt --task_defs.yaml --train_datasets {copied tasklist} --test_datasets {copied tasklist} --tensorboard
  ```
 
4. Get output files from mt-dnn model
   ```bash
   cp mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
5. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files

6. Run Training/assin/get_benchmarks.ipynb
   
    - official scores

##### TweetSentBR
###### TweetSentBR ST-DNN
 1. Run Training/train.ipynb

    - mtdnn calculated scores
    
 2. Run Training/tweetsent/tweet_result.ipynb
 
    -  test output files

 3. Run Training/tweetsent/get_benchmarks.ipynb
   
    - official scores
    
###### TweetSentBR + ASSIN MT-DNN
Colab doesn't support ASSIN MT-DNN.
For more flexible version, see readme in mt-dnn-updated branch.

1. Enter MT-DNN container and mt-dnn_port/Training folder
   
   ```bash
   sudo docker pull allenlao/pytorch-mt-dnn:v0.5
   sudo docker run -it  --mount type=bind,source="$(pwd)",target=/container allenlao/pytorch-mt-dnn:v0.5 bash
   cd /container
   git clone https://github.com/jubs12/mt-dnn_port.git
   cd mt-dnn_port/Training
   bash prepare.sh --tweetsent
   ```
 
2. Preprocess Data
 ```bash
   python prepro_std.py --do_lower_case --root_dir data/canonical_data --task_def task_defs.yaml
 ```
 
3. Train task

```bash
  python train.py  --init_checkpoint mt_dnn_models/mt_dnn_base_uncased.pt --task_defs.yaml --train_datasets {copied tasklist} --test_datasets {copied tasklist} --tensorboard
  ```
 
4. Get output files from mt-dnn model
   ```bash
   cp mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
5. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files

6. Run Training/assin/get_benchmarks.ipynb
   
    - official scores
    
7. Run Training/tweetsent/tweet_result.ipynb
 
    -  test output files

8. Run Training/tweetsent/get_benchmarks.ipynb
   
    - official scores


## Results

Large files are available to download.

### Embeddings

- Reviews titles in b2w

  https://drive.google.com/file/d/1-1uj9IY9KiJMuW9j4qTxHrS6Pw_G6rDP/view?usp=sharing
  
- Faquad

  https://drive.google.com/file/d/184KIIcW3GzfODW7CWdMiEDT_mHPHtXNt/view?usp=sharing
  
## Trained Model

Links in Trained models.md
