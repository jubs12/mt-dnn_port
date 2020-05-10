from io import StringIO
import pandas as pd
import os
import re
import json
import sys

#tweetsentbr eval script requirements
from sklearn.metrics import f1_score
import importlib  
sys.path.append('tweetsentbr/sent-analysis')
from classify import report

mode = sys.argv[1] #'st-dnn', 'mt-dnn_assin+tweetsent'
pretrained = sys.argv[2]

modes = [
    'st-dnn',
    'mt-dnn_assin+tweetsent',
]

pretraineds = [
    'bert_base', 
    'bert-pt_base', 
    'mt-dnn_base', 
    'bert-multilingual_base', 
    'bert_large', 
    'bert-pt_large', 
    'mt-dnn_large',    
]

if mode not in modes:
    raise ValueError(f'Incorrect mode argument: not in {modes}')

if pretrained not in pretraineds:
    raise ValueError(f'Incorrect pretrained argument: not in {pretrained}')

output_dir = f'report/{mode}/{pretrained}'

filepath = \
f'output/{mode}/tweetsent/{pretrained}/tweetsent_test_scores_4.json' if mode == 'st-dnn' \
else  f'output/{mode}/{pretrained}/tweetsent_test_scores_4.json'

with open(filepath) as f:
    output = json.load(f)

rows = list()
headers = ['id', 'prediction']
labels = ['Negative', 'Neutral', 'Positive']

for idx, answer in enumerate(output['predictions']):
    uid = output['uids'][idx]
    label = labels[answer]
    
    rows.append((uid, label)) 

result = pd.DataFrame(rows, columns = headers)

corpora = [f for f in os.listdir('data/dataset/tweetSentBR_extracted') if 'testTT' in f]

tabbed = dict()
for goldpath in corpora:
    with open("data/dataset/tweetSentBR_extracted/{}".format(goldpath)) as f:
        text = f.read()

    assert '\t' not in text 
    
    outtext = re.sub(r'(.+?) (.+)',r'\1\t\2', text)
    tabbed.update({goldpath:StringIO(outtext)})

header = ['id', 'premise']
abbr = {'neg': 'Negative', 'neu': 'Neutral', 'pos': 'Positive'} 
corpus = pd.DataFrame()

for path, f in tabbed.items():
    table = pd.read_csv(f, sep = '\t', names = header)

    posfix = path.split('.')[1]
    label = abbr[posfix]
    table['label'] = label

    corpus = table if corpus.empty else corpus.append(table)

number = {'Negative': 0, 'Neutral': 1, 'Positive': 2}

predictions = list()
i = 0
for corpus_idx, corpus_row in corpus.iterrows():
    uid = corpus_row['id']
    corpus_id_type = corpus['id'].dtype
    result_row  = result.loc[result['id'].astype(corpus_id_type) == uid]
    prediction = result_row.iloc[0]['prediction']
    predictions.append(number[prediction])

with open(f'{output_dir}/tweetsent.json', 'w') as f:
   json.dump(predictions, f) 

number = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
y_test = corpus['label'].map(number)


orig_stdout = sys.stdout
sys.stdout = open(f'{output_dir}/tweetsent_eval.txt', 'w')
report(None, predictions, y_test)
sys.stdout.close()
sys.stdout=orig_stdout

with open(f'{output_dir}/tweetsent_eval.txt') as f:
    print('\n')
    print('tweetsent')
    print(f.read())
