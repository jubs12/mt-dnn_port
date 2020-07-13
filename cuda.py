import pprint
import json
import os

from typing import List

SUFIX = '_test_scores_4.json'
THRESHOLD = 10

GRAD_NORMS = [1.0, 2.0, 5.0]
DROPOUTS = [0.1, 0.3, 0.05]
SEEDS = range(2016,2021)

def read_config(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        config = json.loads(lines[0])
    return config

def check_cuda(mode, pretrained):
    for dropout in DROPOUTS:
        for grad_norm in GRAD_NORMS: 
            for seed in SEEDS:
                folder = f'output/{mode}/{pretrained}/seed/{seed}/grad_norm/{grad_norm}/dropout/{dropout}'
                filepath = f'{folder}/config.json'
                config = read_config(filepath)

                if config['cuda'] != True:
                    print(mode, pretrained, seed, grad_norm, dropout, config['cuda'])

def analysis_cuda(modes: List[str]):
    for mode in modes:
        for pretrained in os.listdir(f'output/{mode}'):
            check_cuda(mode, pretrained)

def main():
    mtdnn = {folder for folder in os.listdir('output') if folder.startswith('mt-dnn')}
    stdnn = {f'st-dnn/{folder}' for folder in os.listdir('output/st-dnn')}
    modes = stdnn | mtdnn

    analysis_cuda(modes)

if __name__ == '__main__':
    main()


