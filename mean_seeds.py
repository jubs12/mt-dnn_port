from copy import copy
import numpy as np
import re
import os
from typing import Iterable, List
from pprint import pprint

assin_idx = [[55, 60], [65, 70], [152, 157], [173, 177]]
tweetsent_idx = [[6, 12], [22, 27], [33, 38], [45, 50]]

def get_metric(task: str, metric_pos: int):
    start, end = metric_pos[0], metric_pos[1] 

    return task[start:end]

def get_idx(task: str):
    sample_metric = get_metric(task, assin_idx[0])

    try:
        float(sample_metric)
        idx = assin_idx
    except ValueError:
        idx = tweetsent_idx

    return idx

def get_metrics(task: str) -> tuple:
    metric_idx = get_idx(task)
    metrics = [get_metric(task, idx) for idx in metric_idx]

    return metrics

def set_metrics(task: str, mean: tuple, std: tuple):
    symbol = '\u00b1'
    metric_idx = get_idx(task)
    rounding = [2, 3, 3, 2] if metric_idx == assin_idx \
               else [4, 3, 3, 3]

    metrics = [
        str(mean[i].round(rounding[i])) +
        symbol +
        str(std[i].round(rounding[i]))
        for i in range(0, 4)
    ]

    reversed_metrics = list(reversed(metrics))
    reversed_idx = reversed(metric_idx)

    for i, idx in enumerate(reversed_idx):
        task = task[0: idx[0]] + reversed_metrics[i] + task[idx[1]:]

    task = re.sub("		              ", "	   ", task)
    
    return task


def get_tasks(report: str):
    tasks = re.split('corpus.*|Saving generated XMLs...', report)
    tasks = [task for task in tasks if re.search(r'\w', task)]

    return tasks


def get_report(filepath: str):
    with open(filepath) as f:
        report = f.read()
        report = re.sub('\n\n\n\n*', '\n\n', report)

    return report


def get_report_mean(scores_lst: List[list], sample):
    scores_arr = np.array(scores_lst).astype(np.float32)
    scores_mean = np.mean(scores_arr, axis=0).round(decimals=5)
    scores_std = np.std(scores_arr, axis=0).round(decimals=5)

    sample = re.sub('Saved evaluation:', 'Evaluation:', sample)
    sample = re.sub('report/', '', sample)
    sample = re.sub('seed/\d*/', '', sample)
    sample = re.sub('_eval.txt', '', sample)
    sample = re.sub('/', ' ', sample)
    sample = re.sub('Saving generated XMLs...', '', sample)

    tasks = tuple(get_tasks(sample))
    tasks_mean = tuple(map(set_metrics, tasks, scores_mean, scores_std))
    report_mean = "\n-------------------------------------------\n".join(
        tasks_mean)
    return report_mean

def save_text(txt: str, outpath: str):
    with open(outpath, 'w') as f:
        f.write(txt)


def main():
    path = 'report/seed'
    pattern = 'cabezudo_2(.*).txt'
    outfile = 'cabezudo_mean.txt'

    scores_lst = list()

    for filename in os.listdir(path):
        if not re.search(pattern, filename):
            continue

        report = get_report(f'{path}/{filename}')
        tasks = get_tasks(report)

        scores = tuple(map(get_metrics, tasks))
        scores_lst.append(scores)

        assert len(scores) == len(scores_lst[0])

    sample = copy(report)
    report_mean = get_report_mean(scores_lst, sample)
    outpath = f'{path}/{outfile}'
    print(f'Saving mean in {outpath}')
    save_text(report_mean, outpath)

if __name__ == '__main__':
    main()
