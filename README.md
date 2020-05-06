# mt-dnn_port
This repository evaluates ST-DNN and MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") on the NLP Portuguese tasks available on [ASSIN](http://nilc.icmc.usp.br/assin/ "ASSIN dataset") and  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository") datasets. 

Please note that Tweetsent formatted data is not available due to Twitter Policy.

## Installation
1. Enter Docker Container
```bash
sudo docker pull allenlao/pytorch-mt-dnn:v0.5
sudo docker run -it --rm --mount type=bind,source="$(pwd)",target=/container \
allenlao/pytorch-mt-dnn:v0.5 bash
```

2. Clone this repository and run prepare.sh
```bash
cd /container
git clone -b organize https://github.com/jubs12/mt-dnn_port.git
cd mt-dnn_port/
bash prepare.sh
```


## Training

MT-DNN was trained on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").  

ST-DNN was executed in Google Colaboratory.

###  ST-DNN
Run st-dnn.ipynb chosing: 

- MODEL from bert-pt, bert, bert-multilingual or mt-dnn
- TYPE from base, large (there is no bert-large-multilingual)
- TASK from assin2-rte, assin2-sts, assin-ptpt-rte, assin-ptpt-sts, assin-ptbr-rte, assin-ptpt-sts or tweetsent

assin-ptbr+2, assin-1+2 (data augmentation tasks) are available only for Portuguese embeddings: bert-pt and bert-multilingual

Or run st-dnn.sh 

```bash
bash st-dnn.sh {MODEL} {TYPE} {TASK}
```

### MT-DNN
Run mt-dnn.sh chosing: 

- MODEL from bert-pt, bert, bert-multilingual or mt-dnn
- TYPE from base, large (there is no bert-large-multilingual)
- TASK from assin, assin+tweetsent, assin-ptbr+assin2, assin2

assin-ptbr+assin2, assin2 are available only for Portuguese embeddings: bert-pt and bert-multilingual

```bash
bash mt-dnn.sh {MODEL} {TYPE} {TASK}
```

## Translation

Translation related codes are available in translate and convert folders. 

Assin dataset translation was  imported from [ruanchaves/assin](https://github.com/ruanchaves/assin/blob/master/sources/dictionary.json) .



##  Results

- Evaluations and scores in reports folder
- Evaluation scripts eval_assin.ipynb and  eval_tensorboard.ipynb
- Model output in output folder
- Assin_xml and tweetsent_json convert model output to answers for evaluation scripts.
- Pretrained models links in pretrained_models.md
- [Tensorboard interactive training graphs](https://colab.research.google.com/drive/14hWbFTv3PsIaVCgk8gqW3pxh_l6_Ap8v) displaying time x dev evaluation.
