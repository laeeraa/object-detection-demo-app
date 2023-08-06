import os
import yaml
from classes.Model import Model
from constants import paths

class ModelHandler: 
    def __init__(self):
        self.models = []
        self.getMMDetModels()
    
    def getMMDetModels(self): 
        models = []
        for dir in os.scandir(paths.MMDET_MODELS):
            if dir.is_dir():
                for file in os.scandir(dir.path): 
                    if file.is_file(): 
                        ext = os.path.splitext(file.path)[-1].lower()
                        gruppe = dir.name
                        if ext == ".yml": 
                            self.parseYamlFile(file.path, gruppe)
            
    def parseYamlFile(self, ymlFile, gruppe): 
        with open(ymlFile) as f:
            result =  yaml.safe_load(f)
            if "Models" in result: 
                models = result["Models"]
                if models != []: 
                    for m in models: 
                        if "Name" in m: 
                            self.models.append(Model(name = m['Name'], group = gruppe))

    def getModels(self): 
        #iterate over models in Model Directory
        for dir in os.scandir(paths.USER_MODELS):
            if dir.is_dir():
                print(dir.path)
                name = dir.name
                configPath = None
                weightPath = None
                for file in os.scandir(dir.path): 
                    if file.is_file(): 
                        ext = os.path.splitext(file.path)[-1].lower() 
                        if ext == ".py": 
                            configPath = file.path
                        elif  ext == ".pth":
                            weightPath = file.path

                if configPath is not None and weightPath is not None: 
                    self.models.append(Model(name, configPath, weightPath))
