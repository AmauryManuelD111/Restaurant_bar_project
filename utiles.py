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

    return pd.json_normalize(json_list)