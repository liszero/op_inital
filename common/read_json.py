import json

def rd_json(filepath):
    with open(filepath,'r',encoding='utf8') as f:
        conf_dt = json.load(f)
    for i in conf_dt:
        i["install"] = i["install"].split(',')
    return conf_dt
