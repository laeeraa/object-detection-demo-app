import yaml
import os
import sys

def mmdetModels(): 
    dir = "./../OpenMMLab/mmdetection/configs"
    models = []
    for dir in os.scandir(dir):
        if dir.is_dir():
            for file in os.scandir(dir.path): 
                if file.is_file(): 
                    ext = os.path.splitext(file.path)[-1].lower()
                    name = dir.name
                    configPath = None
                    weightPath = None
                    if ext == ".yml": 
                        parseYamlFile(file.path)
            
def parseYamlFile(ymlFile): 
    modellist = list()
    with open(ymlFile) as f:
        result =  yaml.safe_load(f)
        if "Models" in result: 
            models = result["Models"]
            if models != []: 
                for m in models: 
                    if "Name" in m: 
                        modellist.append(m['Name'])
        else: 
            return 
        print(modellist)
def main():
    mmdetModels()

if __name__ == '__main__':
    main()
