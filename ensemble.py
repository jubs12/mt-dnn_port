import os
import json
import copy
import pprint
import sys
import re

import numpy as np
from scipy import stats

mode = sys.argv[1]
pretrained = sys.argv[2]

print(mode, pretrained)

# TO DO: unify assin_xml+eval.py verification

assin = [
    'assin2',
    'assin-ptbr',
    'assin-ptpt',
]

ipr = [
    'assin-1+2',
    'assin-ptbr+2',
]

cabezudo = [
    'assin1-rte',
    'best-pt',
    'random-pt',
    'worst-pt',
]

tweetsent = [
    'tweetsent',
]


def add_suffix(tasks, suffix):
    result = [f'{task}-{suffix}' for task in tasks]
    return result


ipr_suffix = add_suffix(ipr, 'rte') + add_suffix(ipr, 'sts')
assin_suffix = add_suffix(assin, 'rte') + add_suffix(assin, 'sts')

pt_only = cabezudo + ipr_suffix

st_dnn_datasets = assin_suffix + pt_only + tweetsent
st_dnn = ['st-dnn/' + dataset for dataset in st_dnn_datasets]

mt_dnn = [
    'mt-dnn_assin2',
    'mt-dnn_assin-ptbr+assin2',
    'mt-dnn_assin',
    'mt-dnn_assin+tweetsent',
]

modes = st_dnn + mt_dnn

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

prefix = f'output/{mode}/{pretrained}'

seeds_dir = f'{prefix}/seed'
seeds = os.listdir(seeds_dir)
sample_seed = seeds[0]

grad_norm_seed_sample_dir = f'{seeds_dir}/{sample_seed}/grad_norm/'
grad_norms = os.listdir(grad_norm_seed_sample_dir)
sample_grad_norm = grad_norms[0]

dropout_grad_norm_seed_sample_dir =  \
    f'{seeds_dir}/{sample_seed}/grad_norm/{sample_grad_norm}/dropout/'
dropouts = os.listdir(dropout_grad_norm_seed_sample_dir)
sample_dropout = dropouts[0]


def is_output(filename):
    match = re.search(r'(.*)_test_scores_(.*).json', filename)

    if not match:
        return False

    epoch, task = match.group(2), match.group(1)
    expected_epoch = '6' if task in cabezudo else '4'

    return epoch == expected_epoch


datasets = [f for f in os.listdir(f"{dropout_grad_norm_seed_sample_dir}/{sample_dropout}")
            if is_output(f)]

output_dir = prefix + '/ensemble/'


def is_rte(dataset: str) -> bool:
    rte_on_name = 'rte' in dataset
    is_cabezudo = dataset in cabezudo
    is_tweetsent = 'tweetsent' in dataset

    return rte_on_name or is_cabezudo or is_tweetsent


def get_key(dataset: str) -> str:
    key = 'predictions' if is_rte(dataset) else 'scores'
    return key


def get_info(dataset: str, seed: str, grad_norm: str, dropout: str) -> dict:
    filename = f'{prefix}/seed/{seed}/grad_norm/{grad_norm}/dropout/{dropout}/{dataset}'

    with open(filename) as f:
        info = json.load(f)

    return info


def average_score(dataset: str, info_lst: list, info_names: list) -> list:
    scores_lst = [info[get_key(dataset)] for info in info_lst]
    wrong = [idx for (idx, scores) in enumerate(scores_lst)
             if len(scores) != len(scores_lst[0])]
    wrong_2 = [idx for (idx, scores) in enumerate(
        scores_lst) if len(scores) == len(scores_lst[0])]

    diff = wrong if len(wrong) < len(wrong_2) else wrong_2

    if len(diff) > 0:
        idx = diff[0]
        print(info_names[idx], len(info_lst[idx]['uids']),
              len(info_lst[idx][get_key(dataset)]))

    scores_arr = np.array(scores_lst)
    scores_avg = stats.mode(scores_arr, axis=0).mode[0] if is_rte(dataset) \
        else np.mean(scores_arr, axis=0)
    scores_avg = scores_avg.tolist()
    assert len(scores_avg) == len(scores_lst[0])

    return scores_avg


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for dataset in datasets:
    info_lst = [get_info(dataset, seed, grad_norm, dropout)
                for seed in seeds for grad_norm in grad_norms for dropout in dropouts]

    info_names = [f'seed = {seed} grad_norm = {grad_norm} dropout = {dropout}'
                  for seed in seeds for grad_norm in grad_norms for dropout in dropouts]

    ensemble = copy.deepcopy(
        get_info(dataset, sample_seed, sample_grad_norm, sample_dropout))
    ensemble[get_key(dataset)] = average_score(dataset, info_lst, info_names)

    with open(f'{output_dir}/{dataset}', 'w') as f:
        json.dump(ensemble, f)
