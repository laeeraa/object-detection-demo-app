import os
import yaml
from classes.Collection import Collection
from constants import paths
import json
from scripts.helpers import get_field
from classes.Model import Model

class ModelHandler: 
    def __init__(self):
        self.collections = []
        self.models = []
        self.collections_filtered = []
        self.models_filtered = []
        self.getMMDetModels()
    
    def getMMDetModels(self): 
        print("Scanning Directory {paths.MMDET_MODELS} for collections and models ... ")
        for dir in os.scandir(paths.MMDET_MODELS):
            if dir.is_dir():
                for file in os.scandir(dir.path): 
                    if file.is_file(): 
                        ext = os.path.splitext(file.path)[-1].lower()
                        coll = dir.name
                        if ext == ".yml": 
                            self.parseYamlFile(file.path, coll)
        print("Finished ")
   
    def parseYamlFile(self, ymlFile, dir): 
        with open(ymlFile) as f:
            json_data =  yaml.safe_load(f)
            if "Collections" in json_data: 
                self.collections.append(self.parseCollection(json_data, dir))

    def parseCollection(self, dict, dir): 
            coll = None
            collection_json = dict.get("Collections")[0]
            if "Name" in collection_json:
                coll = Collection(
                    collection_json.get('Name'),
                    collection_json.get('Metadata'),
                    collection_json.get('Paper'),
                    collection_json.get('README'),
                    collection_json.get('Code')
                )
            else: 
                coll = Collection(name = dir)

            # Create ModelInfo objects for each model in the collection
            for model_data in get_field(dict, "Models"):
                model = Model(
                    get_field(model_data, "Name"),
                    get_field(model_data, "In Collection"),
                    get_field(model_data, "Config"),
                    get_field(model_data, "Metadata"),
                    get_field(model_data, "Weights"),
                )
                for r in  model_data.get("Results"): 
                    model.add_results(
                        r.get("task"),
                        r.get("dataset"), 
                        r.get("metrics")
                    )
                coll.add_model(model)
                self.models.append(model)
            return coll
    
    def find_collection(self,name): 
        for c in self.collections: 
            if c.name == name: 
                return c
        
        return None

    def find_model(self, name): 
        for m in self.models: 
            if m.name == name: 
                return m
        return None