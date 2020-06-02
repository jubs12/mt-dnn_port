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

mode = sys.argv[1]
pretrained = sys.argv[2]
seed = sys.argv[3]

grad_norm = None if len(sys.argv) < 6 else sys.argv[5]
download_folder = 'data/dataset' if len(sys.argv) < 7 else sys.argv[6]
#TO DO: keyword arguments

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

output_dir = f'report/{mode}/{pretrained}/seed/{seed}'
output_dir = f'{output_dir}/grad_norm/{grad_norm}' if grad_norm else output_dir

grad_norm_dir = f'grad_norm/{grad_norm}/' if grad_norm else ''

filepath = \
f'output/{mode}/tweetsent/{pretrained}/seed/{seed}/{grad_norm_dir}tweetsent_test_scores_4.json' if mode == 'st-dnn' \
else  f'output/{mode}/{pretrained}/seed/{seed}/{grad_norm_dir}tweetsent_test_scores_4.json'

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

corpora = [f for f in os.listdir(f'{download_folder}/tweetSentBR_extracted') if 'testTT' in f]

tabbed = dict()
for goldpath in corpora:
    with open(f"{download_folder}/tweetSentBR_extracted/{goldpath}") as f:
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

print('Saving generated JSON...')
if not os.path.exists(output_dir):
        os.makedirs(output_dir)

with open(f'{output_dir}/tweetsent.json', 'w') as f:
   json.dump(predictions, f) 

number = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
y_test = corpus['label'].map(number)

eval_file = f'{output_dir}/tweetsent_eval.txt'

orig_stdout = sys.stdout
sys.stdout = open(eval_file, 'w')
report(None, predictions, y_test)

sys.stdout.close()
sys.stdout=orig_stdout
with open(eval_file) as f:
    print('corpus: TweetSentBR')
    print(f.read())
    print(f'Saved evaluation: {eval_file}\n')
