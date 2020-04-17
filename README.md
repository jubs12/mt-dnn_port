# mt-dnn_port
This repository evaluates ST-DNN and MT-DNN in [specific version](https://github.com/namisan/mt-dnn/tree/60aa9dc4ec1a31532c3f5fb4305c325942c263ce "MT-DNN repository") on the NLP Portuguese tasks available on [Assin](http://nilc.icmc.usp.br/assin/ "Assin dataset") and  [tweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/ "tweetSentBR repository") datasets. 

Please note that Tweetsent formatted data is not available due to Twitter Policy.

## Training

MT-DNN was trained on Google Cloud VM, n1-standard-8, using [mt-dnn container on Docker](https://github.com/namisan/mt-dnn/tree/f444fe9109d5a9980c9d825a24576c8d873bdf33 "MT-DNN repository").  

ST-DNN was executed in Google Colaboratory.

###  ST-DNN

Run stdnn.ipynb chosing: 

- MODEL from bert-pt, bert or mt-dnn 
- TASK from assin2-rte, assin2-sts, assin-ptpt-rte, assin-ptpt-sts, assin-ptbr-rte, assin-ptpt-sts or tweetsent

### MT-DNN

1. Enter Docker Container
```bash
sudo docker pull allenlao/pytorch-mt-dnn:v0.5
sudo docker run -it --rm --mount type=bind,source="$(pwd)",target=/container \
allenlao/pytorch-mt-dnn:v0.5 bash
```

2. Clone this repository
```bash
cd /container
git clone -b mt-dnn-updated https://github.com/jubs12/mt-dnn_port.git
cd mt-dnn_port/
```

3. Run mt-dnn .sh replacing  {model} = bert-pt, bert or mt-dnn

```bash
bash mt-dnn.sh {model} # --tweetsent To include TweetSentBr in training
```

## Translation

Translation related codes are available in translate and convert folders. 

Assin dataset translation was  imported from [ruanchaves/assin](https://github.com/ruanchaves/assin/blob/master/sources/dictionary.json) .



##  Results

- Reports with scores and answers in reports folder
- Evaluation scripts eval_assin.ipynb and  eval_tensorboard.ipynb
- Model output in output folder
- Assin_xml and tweetsent_json convert model output to answers for evaluation scripts.
- Pretrained models links in pretrained_models.md
- [Tensorboard interactive training graphs](https://colab.research.google.com/drive/14hWbFTv3PsIaVCgk8gqW3pxh_l6_Ap8v) displaying time x dev evaluation.





  
