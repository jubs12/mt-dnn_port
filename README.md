# mtdnn_port
This repository evaluates [MT-DNN initial release](https://github.com/namisan/mt-dnn/tree/v0.1 "MT-DNN repository") on the NLP tasks available on the following datasets: [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset"), [B2W-Reviews01](https://github.com/b2wdigital/b2w-reviews01 "B2W repository"), [FaQuAD](https://github.com/liafacom/faquad "faquad repository"), and [MilkQA](http://nilc.icmc.usp.br/nilc/index.php/milkqa/ "MilkQA page"). 

## Translation

The input is translated to English to feed MT-DNN, using the Google Cloud API.

The translation process is shown  in Jupyter notebooks for each task.

## Procedure

Install requirements for mt-dnn

```bash
sh requirements.sh
```

Since b2w is a raw dataset, only embedding extractor is applied to it.

### Embeddings

1. Move input embeddings for B2W  in mt-dnn folder
   ```bash
   mv Embeddings mt-dnn/b2w
   ```

2. Go to folder  
    ```bash
   cd b2w
   ```
   
3. Run extractor

   ```bash
   python extractor.py --do_lower_case --finput b2w/review_title.txt --foutput b2w/review_title.json --bert_model bert-base-uncased --checkpoint mt_dnn_models/mt_dnn_base_uncased.pt
   ```

###  Training



## Results

Larges files are available to download.

### Embeddings

- Reviews titles in b2w

  https://storage.googleapis.com/mtdnn_port/review_title.json
