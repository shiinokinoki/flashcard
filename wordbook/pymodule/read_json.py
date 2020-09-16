import json

def ReadJson(path):
    json_open = open(path, 'r')
    json_load = json.load(json_open)
    return(json_load)