from os import path, makedirs
from subprocess import run, PIPE
import json
import sys

import xmltodict

##### get file from mt-dnn_port repo
mode = sys.argv[1]
dataset = sys.argv[2]
pretrained = sys.argv[3]

seed = None if len(sys.argv) < 5 else sys.argv[4]
grad_norm = None if len(sys.argv) < 6 else sys.argv[5]
download_folder = 'data/dataset' if len(sys.argv) < 7 else sys.argv[6]

test_mode = True if len(sys.argv) == 5 and sys.argv[4] == '--test' else False
ensemble_mode = True if len(sys.argv) == 5 and sys.argv[4] == '--ensemble' else False

seed = None if test_mode or ensemble_mode else seed

modes = [
    'st-dnn',
    'mt-dnn_assin2',
    'mt-dnn_assin-ptbr+assin2',
    'mt-dnn_assin',
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

pt = ['bert-pt_base', 'bert-multilingual_base', 'bert-pt_large']

cabezudo = [
    'assin1-rte',
    'best-pt',
    'random-pt',
    'worst-pt',
]

ipr = [
    'assin-1+2',
    'assin-ptbr+2',
]

pt_only = cabezudo + ipr

assin = ['assin2','assin-ptbr','assin-ptpt']
assin2 = ['assin2']
assin_ptbr_2 = assin2 + ['assin-ptbr']

st_dnn_datasets = assin + pt_only

if mode == 'st-dnn':
    if pretrained not in pt and dataset in pt_only :
        raise ValueError(f'{pt_only} only in {pt} models')
    elif dataset not in st_dnn_datasets:
        raise ValueError(f'{mode} supports {st_dnn_datasets} ASSIN datasets')
elif mode == 'mt-dnn_assin':
    if dataset not in assin:
        raise ValueError(f'{mode} supports {assin} ASSIN datasets')
elif mode == 'mt-dnn_assin2':
    if dataset not in assin2:
        raise ValueError(f'{mode} supports {assin2} ASSIN datasets')
elif mode == 'mt-dnn_assin-ptbr+assin2':
    if dataset not in assin_ptbr_2:
        raise ValueError(f'{mode} supports {assin_ptbr_2} ASSIN datasets')
elif mode == 'mt-dnn_assin+tweetsent':
    if dataset not in assin:
        raise ValueError(f'{mode} supports {assin} ASSIN datasets')

seed_dir = f'seed/{seed}/' if seed else ''
grad_norm_dir = f'grad_norm/{grad_norm}/' if grad_norm else ''

ensemble_dir = f'ensemble/' if seed else ''

if dataset in cabezudo:
    rte_filepath =  f'output/{mode}/{dataset}/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}_test_scores_6.json' if mode == 'st-dnn' \
    else  f'output/{mode}/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}_test_scores_6.json'
else: 
    rte_filepath = \
    f'output/{mode}/{dataset}-rte/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}-rte_test_scores_4.json' if mode == 'st-dnn' \
    else  f'output/{mode}/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}-rte_test_scores_4.json'

if dataset in cabezudo:
    sts_filepath = None
else: 
    sts_filepath = \
    f'output/{mode}/{dataset}-sts/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}-sts_test_scores_4.json' if mode == 'st-dnn' \
    else  f'output/{mode}/{pretrained}/{ensemble_dir}{seed_dir}{grad_norm_dir}{dataset}-sts_test_scores_4.json'

filepaths = {
    'rte': rte_filepath,
    'sts': sts_filepath,
}


output_dir = f'report/{mode}/{pretrained}/'
output_dir = f'{output_dir}/seed/{seed}' if seed else output_dir
output_dir = f'{output_dir}/grad_norm/{grad_norm}' if grad_norm else output_dir

output_dir = f'{output_dir}/ensemble' if ensemble else output_dir

tasks = list()
if rte_filepath:
    tasks.append('rte')

if sts_filepath:
    tasks.append('sts')

scores = dict()

if dataset == 'assin-1+2':
    corpora = ['assin-ptbr', 'assin-ptpt', 'assin2']
elif dataset == 'assin-ptbr+2':
    corpora = ['assin-ptbr', 'assin2']
elif dataset in cabezudo:
    corpora = ['assin-ptbr', 'assin-ptpt']
else:
    corpora = [dataset]

def is_data_augmentation(corpora, mode):
    return len(corpora) >= 2 and mode == 'st-dnn'

print('Saving generated XMLs...')
for corpus in corpora:
    for task in tasks:
        filepath = filepaths[task]
        with open(filepath) as f:
            scores[task] = json.load(f)

    goldfile = 'assin2-blind-test.xml' if corpus == 'assin2' else f'{corpus}-test.xml'
    with open(f'{download_folder}/{goldfile}') as f:
        xml = xmltodict.parse(f.read())

    for idx, item in enumerate(xml['entailment-corpus']['pair']):
        uid = xml['entailment-corpus']['pair'][idx]['@id']
        if is_data_augmentation(corpora, mode): 
            displacement = {
                'assin-ptbr': 10000,
                'assin-ptpt': 20000,
                'assin2': 30000,
            }
            uid = str(int(uid) + displacement[corpus])

        pos = scores['rte']['uids'].index(uid)

        if dataset not in cabezudo:
            similarity = scores['sts']['scores'][pos]
        entailment_labels = ['Entailment','None','Paraphrase']
        entailment = entailment_labels[scores['rte']['predictions'][pos]]

        if dataset not in cabezudo:
            xml['entailment-corpus']['pair'][idx]['@similarity'] = round(similarity, 1)
        xml['entailment-corpus']['pair'][idx]['@entailment'] = entailment

    result = xmltodict.unparse(xml, pretty = True)
    outpath = f'{output_dir}/{dataset}' if is_data_augmentation(corpora, mode) \
    else output_dir 
         
    
    if not path.exists(outpath):
        makedirs(outpath)

    xml_file = f'{outpath}/{corpus}-test.xml'
    with open(xml_file, 'w') as f:
        f.write(result)

    gold_file = f'{download_folder}/{corpus}-test.xml'
    system_file = xml_file
    cmd = ['python', 
           'assin/assin-eval.py', 
           gold_file, 
           system_file
           ] 
    evaluation = run(cmd, stdout=PIPE, stderr=PIPE)
    print(f'corpus: {corpus}')
    print(evaluation.stdout.decode('utf-8'))
    print(evaluation.stderr.decode('utf-8'))
    
    eval_file = f'{outpath}/{corpus}_eval.txt'
    with open(eval_file, 'w') as f:
        f.write(evaluation.stdout.decode('utf-8'))
    print(f'Saved evaluation: {eval_file}')
