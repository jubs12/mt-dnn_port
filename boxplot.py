import re
import os
import sys
import pprint

from typing import Iterable, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text

assin_idx = [[55, 60], [65, 70], [152, 157], [173, 177]]
tweetsent_idx = [[6, 12], [22, 27], [33, 38], [45, 50]]

assin_metrics = [
    'Accuracy',
    'Macro F1',
    'Pearson',
    'Mean Squared Error',
]

tweetsent_metrics = [
    'Accuracy',
    'F1. neg',
    'F1. neu',
    'F1. pos',
]


def is_assin(task_name: str):
    return 'assin' in task_name


def get_idx(task: str, assin: bool):
    idx = assin_idx if assin else tweetsent_idx

    return idx


def get_float(string: str, float_pos: List[int]):
    start, end = float_pos[0], float_pos[1]
    float_num = string[start:end]
    float_num = float(float_num)

    return float_num


def get_metric_name(metric_idx: int, assin: bool):
    metrics_names = assin_metrics if assin else tweetsent_metrics
    metric_name = metrics_names[metric_idx]

    return metric_name


def get_metric(task: str, task_name: str, metric_idx: int) -> tuple:
    task_idx = get_idx(task, is_assin(task_name))[metric_idx]
    metric = get_float(task, task_idx)

    return metric


def get_evals(report: str, task_name: str, model_set: set):
    tasks = re.split('corpus.*|Saving generated XMLs...', report)
    tasks = [task for task in tasks
             if task_name in task and any(model in task for model in model_set)]
    pattern = re.compile(r'report/(.*?/.*?)/.*/dropout/\d+\.\d+(/*.*)/.*?txt')
    evals = {re.search(pattern, task).group(1) + re.search(pattern, task).group(2): task
             for task in tasks}

    return evals


def get_report(filepath: str):
    with open(filepath) as f:
        report = f.read()
        report = re.sub('\n\n\n\n*', '\n\n', report)

    return report


def get_scores_dict(filepath: str, task_name: str, metric_idx: int, model_set: set):
    report = get_report(filepath)
    evals = get_evals(report, task_name, model_set)

    if task_name.startswith('assin') and metric_idx >= 2:
        cabezudo = {
                    'assin1-rte',
                    'best-pt',
                    'random-pt',
                    'worst-pt',
        }

        evals = {key: value for key, value in evals.items()
                    if not any(model in key for model in cabezudo)}


    scores = {key: get_metric(value, task_name, metric_idx)
              for key, value in evals.items()}

    return scores

def adjust_legend(graph, labels, handle_text):
    class TextHandler(HandlerBase):
            def create_artists(self, legend, tup ,xdescent, ydescent,
                                width, height, fontsize,trans):
                tx = Text(
                         width/2.,
                         height/2,
                         tup[0],
                         fontsize=fontsize,
                         ha="center",
                         va="center",
                         #color=tup[1],
                         #fontweight="bold",
                         alpha=1,
                   )
                return [tx]

    graph.set_xticklabels(handle_text)
    label_dict = dict(zip(handle_text, labels))
    handles = [(l, a.get_facecolor()) for l, a in zip(handle_text, graph.artists)]

    graph.legend(handles,
                 labels,
                 bbox_to_anchor=(1, 1),
                 handler_map={tuple : TextHandler()}
                 )

def box_plot(df):
    sns.set(
            font='Open Sans',
            context="paper",
            style="whitegrid",
    )

    fig, graph = plt.subplots()
    fig.subplots_adjust(right=0.65)

    handle_text = range(1, df.shape[1]+1)
    labels = df.columns.values
    color_palette=sns.cubehelix_palette(len(labels), dark=0.2)

    graph = sns.boxplot(data=df,
                        palette=color_palette,
                        showmeans=True,
                        boxprops=dict(alpha=0.5),
                        meanprops=dict(
                                       alpha=1,
                                       markerfacecolor='black',
                                       markeredgecolor='black',
                                       markersize=10,
                                      ),
    )
    adjust_legend(graph, labels, handle_text)

    return fig, graph


def draw_blox_plot(scores_dict_lst: List[dict], task_name: str, metric_idx: int, graph_title: str):
    xlabel = "Aproaches"
    ylabel = get_metric_name(metric_idx, is_assin(task_name))

    df = pd.DataFrame(scores_dict_lst)
    print(df.shape)

    fig, graph = box_plot(df)
    graph.set_title(graph_title)
    graph.set_ylabel(ylabel)
    plt.show()


def main():
    path = 'report/seed'
    models = {
        'en':{
             'mt-dnn_base',
             'bert_base',
             'bert_large',
             'mt-dnn_large',
        },
        'pt':{
            'multilingual',
            'bert-pt_base',
            'bert-pt_large',
        }
    }

    task_name, models_lang, metric_idx, graph_title = sys.argv[1:]

    metric_idx = int(metric_idx)
    model_set = models[models_lang]

    pattern = re.compile(r'\d\d\d\d_.*_.*.txt')
    files = [filename for filename in os.listdir(
        path) if re.search(pattern, filename)]
    scores_dict_lst = [get_scores_dict(
        f'{path}/{filename}', task_name, metric_idx, model_set) for filename in files]
    draw_blox_plot(scores_dict_lst, task_name, metric_idx, graph_title)


if __name__ == '__main__':
    main()
