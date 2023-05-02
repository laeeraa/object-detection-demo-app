import sys
import os

class Model: 
    def __init__(self):
        self.name = ""
        self.configPath = ""
        self.weightPath = ""

    def __init__(self, name, configPath, weightPath):
        self.name = name
        self.configPath = configPath
        self.weightPath = weightPath


class ModelHandler: 
    def __init__(self):
        self.models = []
        self.getModels()

    def getModels(self): 
        dir = "./../models/"
        models = []
        #iterate over models in Model Directory
        for dir in os.scandir(dir):
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
