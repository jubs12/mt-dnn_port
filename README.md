# mtdnn_port
This repository evaluates [MT-DNN initial release](https://github.com/namisan/mt-dnn/tree/v0.1 "MT-DNN repository") on the NLP Portuguese tasks available on the following datasets: [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset"), [B2W-Reviews01](https://github.com/b2wdigital/b2w-reviews01 "B2W repository"), [FaQuAD](https://github.com/liafacom/faquad "faquad repository"), and [MilkQA](http://nilc.icmc.usp.br/nilc/index.php/milkqa/ "MilkQA page").

Most procedures were executed in Google Colaboratory. 

B2W review_title embedding was extracted on Google Cloud VM: n1-standard-8 (8 CPU, memory 30 GB) Ubuntu 16.04.

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

#### Assin
 1. Run Training/train.ipynb for rte and sst
 
    - Get mtdnn calculated scores
 
 2. Get output files from mtdnn model
   ```bash
   mv mt-dnn/checkpoint/{corpus_name}-rte_test_scores_4.json ./results/{corpus_name}-rte_test_scores_4.json
   mv mt-dnn/checkpoint/{corpus_name}-sts_test_scores_4.json ./results/{corpus_name}-sts_test_scores_4.json
   ```
 3. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
   
    - Get assin-formated test output files
 
 4. Run Training/assin/get_benchmarks.ipynb
   
    - Get official scores

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
