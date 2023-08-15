import os
import yaml
from classes.Collection import Collection
from constants import paths
from classes.Model import Model, Result

class ModelHandler: 
    def __init__(self):
        self.collections = []
        self.models = []
        self.collections_filtered = []
        self.models_filtered = []
        self.getMMDetModels()
    
    def getMMDetModels(self): 
        print("Scanning Directory %s for collections and models ... " % (paths.MMDET_MODELS))
        for dir in os.scandir(paths.MMDET_MODELS):
            if dir.is_dir():
                for file in os.scandir(dir.path): 
                    if file.is_file(): 
                        ext = os.path.splitext(file.path)[-1].lower()
                        coll = dir.name
                        if ext == ".yml": 
                            self.parse_yml_file(file.path, coll)
        print("...finished initializing collections and models")
   
    def parse_yml_file(self, ymlFile, dir): 
        with open(ymlFile) as f:
            json_data =  yaml.safe_load(f)
            if "Collections" in json_data: 
                self.collections.append(self.parse_collection(json_data, dir))

    def parse_collection(self, dict, dir): 
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
            if(dict.get("Models")):
                for model_data in dict.get("Models"):
                    model = Model(
                        model_data.get("Name"),
                        model_data.get("In Collection"),
                        model_data.get("Config"),
                        model_data.get("Metadata"),
                        model_data.get("Weights"),
                    )
                    for r in  model_data.get("Results"): 
                        result = Result(r.get("Task"), r.get("Dataset"),  r.get("Metrics"))
                        model.add_results(result)
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