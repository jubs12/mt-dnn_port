# mt-dnn_port
This repository evaluates MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository") on the NLP Portuguese tasks available on the following datasets: [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset"),  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository"),  [B2W-Reviews01](https://github.com/b2wdigital/b2w-reviews01 "B2W repository") , and [FaQuAD](https://github.com/liafacom/faquad "faquad repository").

Most procedures were developed in Google Colaboratory. 

B2W review_title embedding was extracted on Google Cloud VM: n1-standard-8 (8 CPU, memory 30 GB) Ubuntu 16.04 using Anaconda.

The code was also tested on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").

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
   sh requirements.sh
   ```

2. Move input embeddings for B2W to mt-dnn folder


   ```bash
   mv Embeddings/b2w mt-dnn/b2w
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
 ##### ASSIN transfer learning
 1. Run Training/train.ipynb for rte and sst

    - mtdnn calculated scores

 2. Get output files from mtdnn model
   ```bash
   mv mt-dnn/checkpoint/{corpus_name}-rte_test_scores_4.json ./results/{corpus_name}-rte_test_scores_4.json
   mv mt-dnn/checkpoint/{corpus_name}-sts_test_scores_4.json ./results/{corpus_name}-sts_test_scores_4.json
   ```
 3. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
   
    - assin-formated test output files

 4. Run Training/assin/get_benchmarks.ipynb
   
    - official scores

##### ASSIN Multitasking
Colab doesn't support B2W extractor embbedings.

1. Enter MT-DNN container
   
   ```bash
   sudo docker pull allenlao/pytorch-mt-dnn:v0.5
   sudo docker run -it  --mount type=bind,source="$(pwd)",target=/container allenlao/pytorch-mt-dnn:v0.5 bash
   cd /container
   ```
   
2. Enter MT-DNN repository

   ```bash
   git clone https://github.com/namisan/mt-dnn
   git checkout f444fe9109d
   ```

3. Download models and Get task data
   
   ```bash
   bash download.sh
   mv ../move_assin.sh move_assin.sh
   mkdir data/canonical_data
   sh move_assin.sh
   ```
4. Enable Tests scores
   
   ```bash
   patch train.py < ../train.patch
   ```
5. Preprocess data
 
 ```bash
   mv ../prepro_all.sh .
   bash prepro_all.sh --do_lower_case
 ```
 
 6. Train task

```bash
  mv ../train_all.sh .
  bash train_all.sh  mt_dnn_models/mt_dnn_base_uncased.pt --do_lower_case
  ```
 
 7. Get output files from mtdnn model
   ```bash
   mv mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
 8. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files

 9. Run Training/assin/get_benchmarks.ipynb
   
    - official scores



#### Tweetsent
 1. Run Training/train.ipynb

    - mtdnn calculated scores
    
 2. Run Training/tweetsent/tweet_result.ipynb
 
    -  test output files

 3. Run Training/tweetsent/get_benchmarks.ipynb
   
    - official scores

## Results

Large files are available to download.

### Embeddings

- Reviews titles in b2w

  https://drive.google.com/file/d/1-1uj9IY9KiJMuW9j4qTxHrS6Pw_G6rDP/view?usp=sharing
  
- Faquad

  https://drive.google.com/file/d/184KIIcW3GzfODW7CWdMiEDT_mHPHtXNt/view?usp=sharing
  
### Trained mtdnn

- Trained assin-ptbr-rte mtdnn

  https://drive.google.com/file/d/1dzAe1FNVXyaw9gnpqNmXUCD1zvBqPbi8/view?usp=sharing

- Trained assin-ptbr-sts mtdnn

  https://drive.google.com/file/d/1HQkieRBBLS2K9_xE5GJIkPj0LqIJ_xA2/view?usp=sharing

- Trained assin-ptpt-rte mtdnn

  https://drive.google.com/open?id=1cv3Mfk_sPwnjV5dq3wqCQgTDAlnTK8ft

- Trained assin2-rte mtdnn

  https://drive.google.com/file/d/1lGJ4lwyBPpdt04c8KrtSNEm9ztkoFAn4/view?usp=sharing

- Trained assin2-sts mtdnn

  https://drive.google.com/file/d/1-Ny1lJb96bI8iXncT8v0IatLX8QjII3U/view?usp=sharing
  
- Trained assin with multitasking

  https://drive.google.com/file/d/1-9wMA1aC-pq_VrTDi5l1QYmcA60jyQaK/view?usp=sharing
  
- Trained tweetsent mtdnn
  
  https://drive.google.com/file/d/1xJcVceTZe9flknaySdsfOaGXBvVBbyMt/view?usp=sharing
