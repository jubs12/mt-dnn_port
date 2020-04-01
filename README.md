# mt-dnn_port
This repository evaluates MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") on the NLP Portuguese tasks available on [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset") and  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository") datasets.

Most procedures were developed in Google Colaboratory and on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").

This [MTDNN version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") supports Hugging Face Transformers, consequently Portuguese BERT was trained using this branch.
Assin was also executed and there is no difference in performance to master branch.

I was not able to extract embeddings in this [MTDNN version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository").
For that propose please use master branch.



### ASSIN Multitasking

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
   - for portuguese dataset, use --original option in move_assin.sh
   - to include tweetsent, use --tweetsent option in move_assin.sh
   
4. Enable Tests scores
   
   ```bash
   patch train.py < ../train.patch
   ```
5. Preprocess data
 
 ```bash
   mv ../prepro_all.sh .
   bash prepro_all.sh {you can add prepro_std.py options here. eg. ---model neuralmind/bert-base-portuguese-cased}
 ```
 
 6. Train task

```bash
  mv ../train_all.sh .
  bash train_all.sh {you can add train.py options here. eg. ---model bert-base-uncased --do_lower_case --data_dir data/canonical_data/bert_base_uncased_lower}
  ```
 
 7. Get output files from mtdnn model
   ```bash
   mv mt-dnn/checkpoint/*_test_scores_4.json ./result/
   ```
 8. Run Training/assin/assin_result.ipynb, filling corpus = {corpus_name}
    - assin-formated test output files

 9. Run Training/assin/get_benchmarks.ipynb
   
    - official scores
