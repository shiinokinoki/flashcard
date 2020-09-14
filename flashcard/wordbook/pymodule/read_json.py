import json

def ReadJson():
    json_open = open('qitta_json.json', 'r')
    json_load = json.load(json_open)
    return(json_load)