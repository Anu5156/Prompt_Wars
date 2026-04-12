import json

def load_input(file):
    with open(file, 'r') as f:
        return json.load(f)