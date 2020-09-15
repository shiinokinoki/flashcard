import json

def ReadJson():
    json_open = open('../data/json/dict_sample.json', 'r')
    json_load = json.load(json_open)
    return(json_load)