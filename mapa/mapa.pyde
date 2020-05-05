import json
import os

def read_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def setup():
    size(640, 360)
    dirname = os.path.dirname(os.getcwd())
    data = read_data(os.path.join(dirname,'Datos/yuc_coord.json'))
    print(data.keys())



def draw():
    background(200)
    fill(50)
    rect(mouseX, mouseY, 30, 30)
    
