import json

def ler_json(arquivo):
    with open(arquivo, 'r') as f:
        dados = json.load(f)
    return dados

def read_json(arquivo):
    with open(arquivo, 'r') as f:
        dados = json.load(f)
    return dados