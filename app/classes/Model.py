class Model: 
    def __init__(self):
        self.group = ""
        self.name = ""
        self.configPath = None
        self.weightPath = None
        self.architecture = ""
        self.tasks = ""

    def __init__(self, name, configPath=None, weightPath=None, group=""):
        self.name = name
        self.configPath = configPath
        self.weightPath = weightPath
        self.group = group 
