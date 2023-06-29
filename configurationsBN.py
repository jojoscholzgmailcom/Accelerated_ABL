from sampling import *
from generateBN import *
from generateGeneralBN import *

class ConfigurationBN:

    def __init__(self, minNodes, maxNodes, minDep, maxDep) -> None:
        self.minNodes = minNodes
        self.maxDep = maxDep - 1
        self.currentDep = minDep
        self.minDep = minDep
        self.switchComb = [(maxNodes - minNodes), 2 * (maxNodes - minNodes)]
        self.combinations = 2 * (maxNodes - minNodes) + sum(range(minDep - 1, min(maxDep, maxNodes)))
        self.currentCombination = 0
        self.numNodes = minNodes
        self.type = 0
        self.createNetwork = self.createSingleDependencyBayesianNetwork
        
    def updateCombination(self):
        if self.currentCombination == 0:
            self.type = 0
            self.createNetwork = self.createSingleDependencyBayesianNetwork
            self.updateNetwork = self.updateSimple
            self.numNodes = self.minNodes
        elif self.currentCombination in self.switchComb:
            if self.currentCombination == self.switchComb[0]:
                self.type = 1
                self.createNetwork = self.createSingleBayesianNetwork
                self.updateNetwork = self.updateSimple
                self.numNodes = self.minNodes
            else:
                self.type = 2
                self.createNetwork = self.createMultiBayesianNetwork
                self.numNodes = self.minNodes
                self.updateNetwork = self.updateMulti
                self.currentDep = self.minDep
        else:
            self.updateNetwork()
        self.currentCombination += 1
        

    def createBayesianNetwork(self):
        return self.createNetwork()

    def updateSimple(self):
        self.numNodes += 1

    def updateMulti(self):
        if self.currentDep == min(self.maxDep, self.numNodes):
            self.currentDep = self.minDep
            self.numNodes += 1
        else:
            self.currentDep += 1

    def createMultiBayesianNetwork(self):
        return BayesianNetwork(DependenciesMultiLayer(self.numNodes + 1, self.currentDep, self.currentDep))

    def createSingleBayesianNetwork(self):
        return BayesianNetwork(DependenciesMultiLayer(self.numNodes + 1, self.numNodes, self.numNodes))
    
    def createSingleDependencyBayesianNetwork(self):
        return BayesianNetwork(DependencySingleLayer(self.numNodes + 1))