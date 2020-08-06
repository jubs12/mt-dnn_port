import re
import os
import sys
import pprint

from typing import List, Dict

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
             if f'{task_name}_eval.txt' in task and any(model in task for model in model_set)]

    evals = {model: dict() for model in model_set}
    pattern = re.compile(r'report/(.*?)/(.*?)/.*/dropout/\d+\.\d+(/*.*)/.*?txt')
    for task in tasks:
        mode, model, extra = re.search(pattern, task).groups()
        evals[model].update({mode + extra: task})

    return evals


def get_report(filepath: str):
    with open(filepath) as f:
        report = f.read()
        report = re.sub('\n\n\n\n*', '\n\n', report)

    return report


def get_scores_dict(filepath: str, task_name: str, metric_idx: int, model_set: set, cabezudo: bool):
    report = get_report(filepath)
    evals = get_evals(report, task_name, model_set)
    scores = dict()


    if task_name.startswith('assin'):
        cabezudo_approaches = {
                    'st-dnn/assin1-rte',
                    'st-dnn/best-pt',
                    'st-dnn/random-pt',
                    'st-dnn/worst-pt',
            }

        approaches = set(list(evals.values())[0].keys())
        remove_approaches = cabezudo_approaches if metric_idx >= 2 or cabezudo == False else approaches - cabezudo_approaches

    for model in evals:
        for approach in remove_approaches:
            evals[model].pop(approach)

    for model in evals:
        scores[model] = {key: get_metric(value, task_name, metric_idx)
                  for key, value in evals[model].items()}

    return scores

def get_models_scores_dict(files: List[str], task_name: str, metric_idx: int, model_set: set, cabezudo: bool):
        scores_dict_lst = [get_scores_dict(filepath, task_name, metric_idx, model_set, cabezudo)
                            for filepath in files]

        models_scores_dict = dict()
        for model in model_set:
            models_scores_dict[model] = [scores[model] for scores in scores_dict_lst]


        return models_scores_dict


def adjust_legend(graphs, labels, handle_text):
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

    for graph in graphs:
        graph.set_xticklabels(handle_text)

    handles = [(l, a.get_facecolor()) for l, a in zip(handle_text, graphs[0].artists)]

    graph.legend(handles,
                 labels,
                 bbox_to_anchor=(1, 1),
                 handler_map={tuple : TextHandler()}
                 )

def box_plot(dfs):
    sns.set(
            font='Open Sans',
            context="paper",
            style="whitegrid",
    )

    fig, graphs = plt.subplots(1, len(dfs))
    size = fig.get_size_inches()
    fig.set_size_inches(size[0]*2, size[1])

    labels = dfs[0].columns.values
    handle_text = range(1, 1 + len(labels))


    color_palette=sns.cubehelix_palette(len(labels), dark=0.2)

    for idx, df in enumerate(dfs):
        sns.boxplot(ax=graphs[idx],
                    data=df,
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
    adjust_legend(graphs, labels, handle_text)

    return fig, graphs


def draw_blox_plot(model_scores_dict: Dict[str, list], task_name: str, models_lang: str, metric_idx: int):
    xlabel = "Aproaches"
    ylabel = get_metric_name(metric_idx, is_assin(task_name))

    dfs = list()
    for model, scores in model_scores_dict.items():
        df = pd.DataFrame(scores)
        df.name = model
        dfs.append(df)

    fig, graphs = box_plot(dfs)
    for idx, graph in enumerate(graphs):
        graph.set_title(dfs[idx].name)
        graph.set_ylabel(ylabel)

    #fig.tight_layout()
    #plt.savefig(f'boxplot/{task_name}_{models_lang}_{metric_idx}.png')
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
            'bert-multilingual_base',
            'bert-pt_base',
            'bert-pt_large',
        }
    }

    task_name, models_lang, metric_idx = sys.argv[1:4] 
    cabezudo = True if len(sys.argv) == 5 and sys.argv[4] == '--cabezudo' else False

    metric_idx = int(metric_idx)
    model_set = models[models_lang]

    pattern = re.compile(r'\d\d\d\d_.*_.*.txt')
    files = [f'{path}/{filename}' for filename in os.listdir(
        path) if re.search(pattern, filename)]
    models_scores_dict = get_models_scores_dict(files, task_name, metric_idx, model_set, cabezudo)
    draw_blox_plot(models_scores_dict, task_name, models_lang, metric_idx)


if __name__ == '__main__':
    main()
