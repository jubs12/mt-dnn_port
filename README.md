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

# Evaluation
Run prepare_eval.sh and eval.sh choosing: 

- MODEL from bert-pt, bert, bert-multilingual or mt-dnn
- TYPE from base, large (there is no bert-large-multilingual)
- TASK from:
  - st-dnn/assin2-rte, st-dnn/assin2-sts, st-dnn/assin-ptpt-rte, st-dnn/assin-ptpt-sts, st-dnn/assin-ptbr-rte, st-dnn/assin-ptpt-sts or st-dnn/tweetsent
  - mt-dnn_assin, mt-dnn_assin+tweetsent, mt-dnn_assin-ptbr+assin2, mt-dnn_assin2

st-dnn/assin-ptbr+2, st-dnn/assin-1+2 (data augmentation tasks) are available only for Portuguese embeddings: bert-pt and bert-multilingual

mt-dnn_assin-ptbr+assin2, mt-dnn_assin2 are available only for Portuguese embeddings: bert-pt and bert-multilingual

```bash
bash prepare_eval.sh
bash eval.sh {MODE} {MODEL}_{TYPE}
```

# Translation

Translation related codes are available in translate and convert folders. 

Assin dataset translation was  imported from [ruanchaves/assin](https://github.com/ruanchaves/assin/blob/master/sources/dictionary.json) .

#  Results

Evaluations and scores are in reports folder
