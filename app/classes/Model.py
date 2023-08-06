class Model:
    def __init__(self, name, collection, config, metadata, results, weights):
        self.name = name
        self.collection = collection
        self.config = config
        if(metadata != None): self.metadata = metadata
        self.results = results
        self.weights = weights

    def __str__(self):
        return f"Name: {self.name}\nIn Collection: {self.collection}\nConfig: {self.config}\nMetadata: {self.metadata}\nResults: {self.results}\nWeights: {self.weights}"

