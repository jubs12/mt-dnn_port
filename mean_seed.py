from copy import copy
import numpy as np
import re
import os
from typing import Iterable
from pprint import pprint

assin_report = \
    r"""RTE evaluation
Accuracy	Macro F1
--------	--------
  (.....)%	   (.....)

Similarity evaluation
Pearson		Mean Squared Error
-------		------------------
  (.....)		              (....)"""

tweetsent_report = \
    r"""Acc: (......)
F1. neg: (.....) neu: (.....) post: (.....)
Acc dist min: (......)
Acc dist max: (......)
Acc dist min equal: (......)
Acc dist max equal: (......)"""

rounding_assin = [2, 3, 3, 2]
rounding_tweetsent = [5, 3, 3, 3]


def assin_match(task: str):
    return re.search(assin_report, task)


def tweetsent_match(task: str):
    return re.search(tweetsent_report, task)


def get_metrics(task: str) -> tuple:
    match = assin_match(task) if assin_match(task) else tweetsent_match(task)

    if not match:
        raise ValueError('Task report not in ASSIN or TweetSentBR format')

    metrics = [match.group(i) for i in range(1, 5)]

    return metrics


def set_metrics(task: str, mean: tuple, std: tuple):
    symbol = '\u00b1'
    rounding = rounding_assin if assin_match(task) else rounding_tweetsent

    metrics_sample = tuple(get_metrics(task))
    metrics_final = [
        str(mean[i].round(rounding[i])) +
        symbol +
        str(std[i].round(rounding[i]))
        for i in range(0, 4)
    ]

    for idx, metric in enumerate(metrics_sample):
        task = re.sub(metric, metrics_final[idx], task)

    #task = re.sub("\n  ", "\n", task)
    #task = re.sub(r"	   ([0-9])", r"	\1", task)
    #task = re.sub(r"		              ([0-9])", r"	\1", task)

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


def get_report_mean(scores_lst: List[list])


scores_arr = np.array(scores_lst).astype(np.float32)
scores_mean = np.mean(scores_arr, axis=0).round(decimals=5)
scores_std = np.std(scores_arr, axis=0).round(decimals=5)

sample = copy(report)
sample = re.sub('Saved evaluation:', 'Evaluation:', sample)
sample = re.sub('report/', '', sample)
sample = re.sub('seed/.*/', '', sample)
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
    pattern = 'seed_2(.*).txt'
    outfile = 'seed_mean.txt'

    scores_lst = list()

    for filename in os.listdir(path):
        if not re.search(pattern, filename):
            continue

        report = get_report(f'{path}/{filename}')
        tasks = get_tasks(report)

        scores = tuple(map(get_metrics, tasks))
        scores_lst.append(scores)

        assert len(scores) == len(scores_lst[0])

    report_mean = get_report_mean(scores_lst, sample)
    save_text(report_mean, f'{path}/{outfile}')
