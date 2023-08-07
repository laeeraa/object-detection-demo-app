
class Metadata:
    def __init__(self, training_memory_gb="", epochs=""):
        self.training_memory_gb = training_memory_gb
        self.epochs = epochs

    def __str__(self):
        return f"Training Memory (GB): {self.training_memory_gb}\nEpochs: {self.epochs}"

class Results:
    def __init__(self, task, dataset, metrics):
        self.task = task
        self.dataset = dataset
        self.metrics = metrics

def __str__(self):
        metrics_str = ", ".join([f"{key}: {value}" for key, value in self.metrics.items()])
        return f"Task: {self.task}\nDataset: {self.dataset}\nMetrics: {metrics_str}"


class Model:
    def __init__(self, name, collection, config, metadata, weights):
        self.name = name
        self.collection = collection
        self.config = config
        if(metadata != None): self.metadata = Metadata(metadata.get("Training Memory GB"), metadata.get("Epochs")) 
        else: self.metadata = Metadata()
        self.results = []
        self.weights = weights

    def add_results(self, task, dataset, metrics):
        result = Results(task, dataset, metrics)
        self.results.append(result)

    def __str__(self):
        return f"Name: {self.name}\nIn Collection: {self.collection}\nConfig: {self.config}\nMetadata: {self.metadata}\nResults: {self.results}\nWeights: {self.weights}"

