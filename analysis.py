import statistics
import pprint
import json
import os

from typing import List

SUFIX = '_test_scores_4.json'
THRESHOLD = 10

GRAD_NORMS = [1.0, 2.0, 5.0]
DROPOUTS = [0.1, 0.3, 0.05]
SEEDS = range(2016,2021)

def get_metrics(mode,pretrained, grad_norm, dropout):
    global COUNT
    global TOTAL

    metrics = dict()
    for seed in SEEDS:
        folder = f'output/{mode}/{pretrained}/seed/{seed}/grad_norm/{grad_norm}/dropout/{dropout}'
        filenames = [f for f in os.listdir(folder) if f.endswith(SUFIX)]
        
        for filename in filenames:
            filepath = f'{folder}/{filename}'
            with open(filepath) as f:
                info = json.load(f)
        
            task = filename.replace(SUFIX, '')
            main_metric = 'ACC' if 'ACC' in info['metrics'].keys() else 'Pearson'
            
            if not info['metrics']:
                return None
            else:
                TOTAL = TOTAL + 1


            task_metric = info['metrics'][main_metric]

            if task not in metrics.keys():
                metrics[task] = {'metrics': [task_metric]}
            else: 
                metrics[task]['metrics'].append(task_metric) 

    for task in metrics.keys():
        avg = statistics.mean(metrics[task]['metrics'])
        std = statistics.stdev(metrics[task]['metrics'])

        metrics[task].update({'avg': avg, 'std': std})

        outliers = [seed for (idx, seed) in enumerate(SEEDS) 
                    if abs(metrics[task]['metrics'][idx] - avg) > THRESHOLD]

        COUNT += len(outliers)

        if len(outliers) > 0:
            print(f'seeds = {outliers} grad_norm = {grad_norm} dropout = {dropout} mode = {mode} pretrained {pretrained}')

        metrics[task].update({'outliers': outliers})

    return metrics

def analysis_outliers(modes: List[str]):
    global COUNT
    global TOTAL
    COUNT = 0
    TOTAL = 0

    result = dict()
    for mode in modes:
        result[mode] = dict()
        for pretrained in os.listdir(f'output/{mode}'):    
            result[mode][pretrained] = {grad_norm: 
                                {dropout: get_metrics(mode,pretrained, grad_norm, dropout) for dropout in DROPOUTS}
                                for grad_norm in GRAD_NORMS}

    print(f'Outliers: {COUNT} - {COUNT/TOTAL*100}%')
    print(f'Threshould: {THRESHOLD}%')

basic_params = [
 'log_file',
 'data_sort_on',
 'name',
 'glue_format_on',
 'update_bert_opt',
 'multi_gpu_on',
 'mem_cum_type',
 'answer_num_turn',
 'answer_mem_drop_p',
 'answer_att_hidden_size',
 'answer_att_type',
 'answer_rnn_type',
 'answer_sum_att_type',
 'answer_merge_opt',
 'answer_mem_type',
 'max_answer_len',
 'answer_dropout_p',
 'answer_weight_norm_on',
 'dump_state_on',
 'answer_opt',
 'mtl_opt',
 'ratio',
 'mix_opt',
 'max_seq_len',
 'init_ratio',
 'encoder_type',
 'num_hidden_layers',
 'bert_model_type',
 'do_lower_case',
 'masked_lm_prob',
 'short_seq_prob',
 'max_predictions_per_seq',
 'log_per_updates',
 'save_per_updates',
 'save_per_updates_on',
 'epochs',
 'batch_size',
 'batch_size_eval',
 'optimizer',
 'grad_clipping',
 'weight_decay',
 'learning_rate',
 'momentum',
 'warmup',
 'warmup_schedule',
 'adam_eps',
 'vb_dropout',
 'dropout_w',
 'bert_dropout_p',
 'model_ckpt',
 'resume',
 'have_lr_scheduler',
 'multi_step_lr',
 'freeze_layers',
 'embedding_opt',
 'lr_gamma',
 'bert_l2norm',
 'scheduler_type',
 'grad_accumulation_step',
 'fp16',
 'fp16_opt_level',
 'vocab_size',
 'hidden_size',
 'hidden_act',
 'intermediate_size',
 'hidden_dropout_prob',
 'attention_probs_dropout_prob',
 'max_position_embeddings',
 'type_vocab_size',
 'initializer_range',
 'tensorboard',
 'tensorboard_logdir',
 ]

huggingface_params = [
 'output_attentions',
 'output_hidden_states',
 'torchscript',
 'use_bfloat16',
 'pruned_heads',
 'is_encoder_decoder',
 'is_decoder',
 'min_length',
 'max_length',
 'do_sample',
 'early_stopping',
 'num_beams',
 'temperature',
 'top_k',
 'top_p',
 'repetition_penalty',
 'length_penalty',
 'no_repeat_ngram_size',
 'num_return_sequences',
 'prefix',
 'bos_token_id',
 'pad_token_id',
 'eos_token_id',
 'decoder_start_token_id',
 'model_type',
 'layer_norm_eps',
 'architectures',
 'num_return_sequences',
 'prefix',
 'decoder_start_token_id',
 'model_type',
  'num_attention_heads',
  'mkd_opt',
   'encode_mode',          
]

new_params =  [
 'use_cache',
 'xla_device',
 'bad_words_ids',
]

common_params = basic_params + huggingface_params + new_params

common_task_params = [
 'task_def_list',
 'task_def',
 'train_datasets',
 'test_datasets',              
]

task_params_huggingface  = [ 
'task_specific_params',
'finetuning_task',
'id2label',
 'label2id',
]

task_params = common_task_params + task_params_huggingface 

specific_params = [
 'init_checkpoint',
 'global_grad_clipping',
 'dropout_p',
 'seed',                 
]

specific_params_dict = {
    'init_checkpoint': 'pretrained',
    'global_grad_clipping': 'grad_norm',
    'dropout_p': 'dropout',
    'seed': 'seed',
}

model_name2folder_name = {
    'mt_dnn_models/mt_dnn_large_uncased.pt': 'mt-dnn_large',
    'mt_dnn_models/mt_dnn_base_uncased.pt': 'mt-dnn_base',
    'bert-base-uncased': 'bert_base',
    'bert-large-uncased': 'bert_large',
    'bert-base-multilingual-cased': 'bert-multilingual_base',
    'neuralmind/bert-large-portuguese-cased': 'bert-pt_large',
    'neuralmind/bert-base-portuguese-cased': 'bert-pt_base',
}

no_matter = [
 'output_dir',
 'data_dir',
 'cuda',
]

cased_params = [
    'pooler_num_fc_layers', 
    'directionality', 
    'pooler_num_attention_heads', 
    'pooler_type', 
    'pooler_size_per_head', 
    'pooler_fc_size',
]

extra_params = [
    'output_past',
    '_num_labels',
]

old_params = [
    'kd_loss_types',
    'tasks_dropout_p', 
    'task_types', 
    'label_size',
    'loss_types',
]

params = common_params + task_params + specific_params

def read_config(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        config = json.loads(lines[0])
    return config

def check_params_keys(pretrained, seed, grad_norm, dropout, config):
    considered_params = set(params + extra_params + no_matter)
    all_params = set(config.keys())

    is_cased = check_cased_params_keys(pretrained, all_params, considered_params, cased_params)
    is_old = check_old_params_keys(pretrained, seed, grad_norm, dropout, all_params, considered_params, old_params)

    assert len(all_params - considered_params) == 0 or is_cased or is_old

    return is_cased, is_old

def check_cased_params_keys(pretrained, all_params, considered_params, bert_pt_params):
    is_cased = pretrained.startswith('bert-pt') or pretrained.startswith('bert-multilingual')
    check_params = len(all_params - considered_params - set(cased_params)) == 0

    return is_cased and check_params

def check_old_params_keys(pretrained, seed, grad_norm, dropout, all_params, considered_params, old_params):
    is_old_mt_dnn_version = seed == 2018 and grad_norm == 1.0 and dropout == 0.1 and 'large' not in pretrained
    check_params = len(all_params - considered_params - set(old_params)) == 0

    return is_old_mt_dnn_version and check_params

def check_specific_param_values(pretrained, seed, grad_norm, dropout, config):
    for specific_param in specific_params:
        param = config[specific_param]

        if specific_params_dict[specific_param] == 'seed':
            assert param == seed
        elif specific_params_dict[specific_param] == 'pretrained':
            assert model_name2folder_name[param] == pretrained
        elif specific_params_dict[specific_param] == 'grad_norm':
            assert param == grad_norm
        elif specific_params_dict[specific_param] == 'dropout':
            assert param == dropout
        else:
            msg = f'Specific parameter {specific_param} not in {specific_params_dict}'
            raise KeyError(msg)

def get_sub_params(config, sub_params_list):
    sub_params = {key: config[key] for key in sub_params_list}
    return sub_params

def not_shared_items(x: dict, y: dict):
    not_common = [k for k in x if k in y and x[k] != y[k]]
    return not_common

def check_task_param_values(pretrained, config, is_old_version, dict_task_common, dict_task_huggingface): 
    if not (pretrained.startswith('mt-dnn') and is_old_version):
        config_task_param = get_sub_params(config, common_task_params)
        if not dict_task_common:
            dict_task_common = config_task_param

        diffs = not_shared_items(config_task_param, dict_task_common)
        if 'task_def' in diffs:
            diffs.remove('task_def') #task definition location
        
        for diff in diffs: 
            if diff == 'task_def_list':
                for item in config_task_param[diff]:
                    item.pop('label_vocab', None)

                for item in dict_task_common[diff]:
                    item.pop('label_vocab', None)

                if config_task_param[diff] != dict_task_common[diff]:
                    assert 'train_datasets' in diffs or 'test_dasets' in diffs
                    set_list1 = set(tuple(sorted(d.items())) for d in config_task_param[diff])
                    set_list2 = set(tuple(sorted(d.items())) for d in dict_task_common[diff])
                    assert set_list1 == set_list2
            elif isinstance(config_task_param[diff], list): #'train_datasets' or 'test_dasets'
                assert set(config_task_param[diff]) == set(dict_task_common[diff])
            else:
                msg = f'Unexpected difference in {diff}'
                raise ValueError(msg)

    if not pretrained.startswith('mt-dnn'):
        config_task_param = get_sub_params(config, task_params_huggingface)
        if not dict_task_huggingface:
            dict_task_huggingface = config_task_param  
        assert config_task_param == dict_task_huggingface
    
    return dict_task_common, dict_task_huggingface

def check_common_param_values(pretrained, seed, grad_norm, dropout, config, is_old_version, dict_common, dict_huggingface):
    config_common_param = get_sub_params(config, basic_params)
    if dict_common == None:
        dict_common = config_common_param
    diffs = not_shared_items(config_common_param, dict_common)
    if 'fp16_opt_level' in diffs:
        diffs.remove('fp16_opt_level')
    if 'fp16' in diffs:
        diffs.remove('fp16')
    if 'answer_opt' in diffs:
        diffs.remove('answer_opt')
    
    if len(diffs) > 0:
        for diff in diffs:
            print(mode, pretrained, seed, grad_norm, dropout)
            print(diff, config_common_param[diff], dict_common[diff])

    if not pretrained.startswith('mt-dnn'):
        config_huggingface = get_sub_params(config, huggingface_params)
        if not dict_huggingface:
            dict_huggingface = config_huggingface
        assert dict_huggingface == config_huggingface

    return dict_common, dict_huggingface

def check_task_params(mode, pretrained):
    #print(mode, pretrained)
    dict_common = None
    dict_huggingface = None
    dict_task_common = None
    dict_task_huggingface = None 
    for grad_norm in GRAD_NORMS: 
        for dropout in DROPOUTS:
            for seed in SEEDS:
                folder = f'output/{mode}/{pretrained}/seed/{seed}/grad_norm/{grad_norm}/dropout/{dropout}'
                filepath = f'{folder}/config.json'
                config = read_config(filepath)

                _, is_old_version = check_params_keys(pretrained, seed, grad_norm, dropout, config)
                check_specific_param_values(pretrained, seed, grad_norm, dropout, config)
                dict_task_common, dict_task_huggingface = check_task_param_values(pretrained, config, is_old_version, dict_task_common, dict_task_huggingface)
                dict_common, dict_huggingface = check_common_param_values(pretrained, seed, grad_norm, dropout, config, is_old_version, dict_common, dict_huggingface)

    return dict_common, dict_huggingface

def check_pretrained_params(result_a, result_b, specs: list):
    diffs = not_shared_items(result_a, result_b)
    for spec in specs:
        if diffs and spec in diffs:
            diffs = diffs.remove(spec)
    if diffs:
        print(f'Parameters differs in {diffs}')

def analysis_params(modes: List[str]):
    results = dict()
    for mode in modes:
        pretraineds = os.listdir(f'output/{mode}')
        results[mode] = [check_task_params(mode, pretrained) for pretrained in pretraineds]

        model_specific = [
                       ['num_hidden_layers', 'vocab_size', 'hidden_size', 'intermediate_size'],
                       ['num_attention_heads'],
        ]
        
        sample = None
        for result in results[mode]:
            if not sample:
                sample = result
            for idx in [0,1]:
                if result[idx] and sample[idx]: 
                    check_pretrained_params(result[idx], sample[idx], model_specific[idx])

    sample = None
    for mode in modes:
        if not sample:
            sample = results[mode][0]
        for idx in [0,1]:
            if result[idx] and sample[idx]: 
                check_pretrained_params(results[mode][0][idx], sample[idx], model_specific[idx])

def main():
    mtdnn = {folder for folder in os.listdir('output') if folder.startswith('mt-dnn')}
    stdnn = {f'st-dnn/{folder}' for folder in os.listdir('output/st-dnn')}
    modes = stdnn | mtdnn

    cabezudo = {
    'st-dnn/assin1-rte',
    'st-dnn/best-pt',
    'st-dnn/worst-pt',
    'st-dnn/random-pt',
    }


    analysis_outliers(modes)
    print('Analising parameters...')
    print('If not is printed, parameters are ok')
    analysis_params(modes - cabezudo)
    analysis_params(cabezudo)

if __name__ == '__main__':
    main()


