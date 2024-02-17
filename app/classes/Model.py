
class Metadata:
    def __init__(self, training_memory_gb="", epochs="", inference_time=None):
        self.training_memory_gb = training_memory_gb
        self.epochs = epochs
        if(inference_time != None and inference_time != ""):
            self.inference_time = inference_time[0]
        else: self.inference_time = None

    def __str__(self):
        inference_str = "None"
        if(self.inference_time != None): 
            inference_str = ", ".join([f"{key}: {value}" for key, value in self.inference_time.items()])

        return f"Training Memory (GB): {self.training_memory_gb}\nEpochs: {self.epochs}\nInference time: {inference_str}"

class Result:
    def __init__(self, task, dataset, metrics):
        self.task = task
        self.dataset = dataset
        self.metrics = metrics

    def __str__(self):
            metrics_str = "None"
            if(self.metrics != None): 
                metrics_str = ", ".join([f"{key}: {value}" for key, value in self.metrics.items()])
            return f"Task: {self.task}\nDataset: {self.dataset}\nMetrics: {metrics_str}"


class Model:
    def __init__(self, name, collection, config, metadata, checkpoint):
        self.name = name
        self.collection = collection
        self.config = config
        if(metadata != None): self.metadata = Metadata(metadata.get("Training Memory GB"), metadata.get("Epochs"), metadata.get("inference time (ms/im)")) 
        else: self.metadata = Metadata()
        self.results = []
        self.checkpoint = checkpoint

    def add_results(self, result):
        self.results.append(result)

    def __str__(self):
        results_str = "\n".join([f"- {result}" for result in self.results])
        return f"Name: {self.name}\nIn Collection: {self.collection}\nConfig: {self.config}\nMetadata: {self.metadata}\nResults: {results_str}\nWeights: {self.checkpoint}"

