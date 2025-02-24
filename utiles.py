import json
import os
import pandas as pd

def json_loader(route):
    json_list = []
    for root , _, files in os.walk(route):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root,filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    json_list.append(json.load(file))
    return json_list       

def mean(list, key=lambda x: x):
    new = []
    for i in list:
        new.append(key(i))
    suma = sum(new)
    total = len(new)
    return suma/total if total > 0 else None

def obtener_df(json_list):
    for i,v in enumerate(json_list):
        lazo = ''
        if 'type' not in v and not v['type']:
            v['type'] = []
        v['type'].sort()
        
        for x in v['type']:
            if not x:
                print(v)
                continue
            lazo += x
        json_list[i]['type'] = lazo

        json_list[i]['contact']['phone'] = True if v['contact']['phone'] else False
        json_list[i]['contact']['facebook'] = True if v['contact']['facebook'] else False
        json_list[i]['contact']['instagram'] = True if v['contact']['instagram'] else False
        json_list[i]['contact']['website'] = True if v['contact']['website'] else False

        for key,val in v['menu'].items():
            if key:
                dict_min = {}
                dict_max = {}
                value_mean = None
                try:
                    dict_min = min(val, key=lambda x: float(x['price']))
                except: pass
                json_list[i][f'menu_{key}_min'] = dict_min.get('price', None)
                try:
                    dict_max = max(val, key=lambda x: float(x['price']))
                except: pass
                json_list[i][f'menu_{key}_max'] = dict_max.get('price', None)
                try:
                    value_mean = mean(val, key=lambda x: float(x['price']))
                except: pass
                json_list[i][f'menu_{key}_mean'] = value_mean if value_mean else None
                

        


    return pd.json_normalize(json_list)

if __name__ == '__main__':
    df = obtener_df(json_loader('jsons'))