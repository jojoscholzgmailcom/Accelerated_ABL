import math
import sampling

class DependenciesSingleLayer:

    def __init__(self, num_nodes, dependencies):
        self.num_nodes = num_nodes
        self.dependencies = dependencies
        
    def generateNetwork(self, model):
        nodesLeft = self.num_nodes
        for idx in range(math.ceil(self.num_nodes / (self.dependencies + 1))):
            self.createDependencies(model, nodesLeft, self.dependencies + 1)
            nodesLeft -= self.dependencies + 1

    def createDependencies(self, model, nodesLeft, dependencies):
        if nodesLeft < dependencies:
            dependencies = nodesLeft
        startIdx = len(model.nodes)
        for i in range(dependencies - 1):
            model.nodes.append(sampling.BooleanNode(len(model.nodes), [], False))
        model.nodes.append(sampling.BooleanNode(len(model.nodes), [startIdx + x for x in range(dependencies - 1)], True))

class DependencySingleLayer:

    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        
    def generateNetwork(self, model):
        for idx in range(self.num_nodes - 1):
            model.nodes.append(sampling.BooleanNode(len(model.nodes), [], False))
        model.nodes.append(sampling.BooleanNode(len(model.nodes), [len(model.nodes) - 1], True))
            
        