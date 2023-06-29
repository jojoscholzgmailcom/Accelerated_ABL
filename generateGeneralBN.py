import math
import sampling
import random

class DependenciesMultiLayer:

    def __init__(self, num_nodes, min_dependencies, max_dependencies):
        self.num_nodes = num_nodes
        self.min_dependencies = min_dependencies
        self.max_dependencies = max_dependencies
        
        
    def generateNetwork(self, model):
        self.nodesLeft = self.num_nodes - 1
        self.generateParents(model, True)

    def generateParents(self, model, isDecision):
        parents = []
        numParents = min(random.randint(self.min_dependencies, self.max_dependencies), self.nodesLeft)
        self.nodesLeft -= numParents
        for _ in range(numParents):
            parent = self.generateParents(model, False)
            if parent != None:
                parents.append(parent)
        model.nodes.append(sampling.BooleanNode(len(model.nodes), parents, isDecision))
        return len(model.nodes) - 1