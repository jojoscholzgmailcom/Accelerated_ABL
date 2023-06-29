import random
import itertools
import math
import networkx as nx
import matplotlib.pyplot as plt
from sys import exit

class BooleanNode:

    def __init__(self, nodeIdx, parents, isDecision):
        self.nodeIdx = nodeIdx
        self.parents = parents
        self.probabilityDict = {}
        if len(parents) > 0:
            self.initwithParams(isDecision)
        else:
            self.probabilityDict[None] = random.random()

    def initwithParams(self, isDecision):
        perm = list(itertools.product([0,1], repeat = len(self.parents)))
        #allTrue = tuple([1 for x in range(len(self.parents))])
        #chosen_idx = random.randrange(0, len(perm)) #int(len(perm) / 2) 
        for idx in range(len(perm)):
            if sum(perm[idx]) % 2 == 0 and isDecision:
                self.probabilityDict[perm[idx]] = 1
            else:
                if isDecision:
                    self.probabilityDict[perm[idx]] = 0
                else:
                    self.probabilityDict[perm[idx]] = random.random()

    def getValue(self, state):
        if len(self.parents) == 0:
            if random.random() < self.probabilityDict[None]:
                return 1
            else:
                return 0
        parentsActive = tuple([state[self.parents[x]] for x in range(len(self.parents))])
        if random.random() < self.probabilityDict[parentsActive]:
            return 1
        else:
            return 0
    
    def getProbability(self, state):
        if len(self.parents) == 0:
            if state[self.nodeIdx] == 1:
                return self.probabilityDict[None]
            else:
                return 1 - self.probabilityDict[None]
        parentsActive = tuple([state[self.parents[x]] for x in range(len(self.parents))])
        if state[self.nodeIdx] == 1:
            return self.probabilityDict[parentsActive]
        else:
            return 1 - self.probabilityDict[parentsActive]

class BayesianNetwork:

    def __init__(self, generator):
        self.nodes = []
        self.parents = []
        self.nonParents = []
        generator.generateNetwork(self)
        for idx in range(len(self.nodes)):
            if len(self.nodes[idx].parents) == 0:
                self.parents.append(idx)
            else:
                self.nonParents.append(idx)

    def generateState(self):
        state = list([-1 for x in range(len(self.nodes))])
        for idx in range(len(self.parents)):
            state[self.parents[idx]] = self.nodes[self.parents[idx]].getValue(state)
        for idx in range(len(self.nonParents)):
            state[self.nonParents[idx]] = self.nodes[self.nonParents[idx]].getValue(state)
        if (-1 in state):
            exit("Error: State not filled correctly!")
        return tuple(state)

    def generateStates(self, amount):
        states = []
        for _ in range(amount):
            states.append(self.generateState())
        return states

    def getFullProbabilities(self):
        perm = list(itertools.product([0,1], repeat = len(self.nodes)))
        print(len(self.nodes), perm)
        fullProbabilities = {}
        for comb in perm:
            fullProbabilities[comb] = 1
            for node in self.nodes:
                fullProbabilities[comb] *= node.getProbability(comb)
        return fullProbabilities
    
    def numTotalDependencies(self) -> int:
        numDep = 0
        for node in self.nodes:
            numDep += len(node.parents)
        return numDep
    
    def numLastDependency(self) -> int:
        return len(self.nodes[len(self.nodes) - 1].parents)
    
    def showNetwork(self) -> None:
        G = nx.DiGraph()
        G.add_nodes_from([idx for idx in range(len(self.nodes))])
        for node in self.nodes:
            for parent in node.parents:
                G.add_edge(parent, node.nodeIdx)
        pos = nx.spring_layout(G)
        nx.draw_networkx_labels(G, pos)
        nx.draw(G, pos, arrows = True)
        plt.show()


"""
def sampleFromDist(amount, distribution):
    return random.choices(range(0, len(distribution)), weights = distribution, k = amount)

def generateDependentExamples(numData, nodes, numDependecies):
    bayesian = BayesianNetwork(nodes, numDependecies)
    distribution = list(bayesian.getFullProbabilities().values())
    print(distribution)
    return sampleFromDist(numData, distribution)

print(generateDependentExamples(20, 3, 2))
"""