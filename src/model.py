"""
Record for the parameters of a random graph model
Currently it can be either erdos renyi or random power law graph
the field name indicates the model
"""
from utils import printts

class Model:
    """ """
    def __init__(self):
        pass

    def erdos_renyi(self, num_nodes, prob):
        """ erdos renyi model """
        self.name = "erdosrenyi"
        self.num_nodes = num_nodes
        self.prob = prob

    def random_power_law(self, num_nodes, max_deg, avg_deg, gamma):
        """ random power law graph model """
        self.name = "randompowerlawgraph"
        self.num_nodes = num_nodes
        self.max_deg = max_deg
        self.avg_deg = avg_deg
        self.gamma = gamma

    def print_arguments(self):
        """ prints arguments of the model """
        if self.name == "randompowerlawgraph":
            printts("Random power law graph model:")
            printts("Num nodes: "+str(self.num_nodes))
            printts("Max deg: "+str(self.max_deg))
            printts("Avg deg: "+str(self.avg_deg))
            printts("gamma: "+str(self.gamma))
        else:
            printts(self.name)

def erdos_renyi_model(num_nodes, prob):
    """ wrapper for the Model 'factory' method """
    model = Model()
    model.erdos_renyi(num_nodes, prob)
    return model

def random_power_law_model(num_nodes, max_deg, avg_deg, gamma):
    """ wrapper for the Model  'factory' method """
    model = Model()
    model.random_power_law(num_nodes, max_deg, avg_deg, gamma)
    return model
