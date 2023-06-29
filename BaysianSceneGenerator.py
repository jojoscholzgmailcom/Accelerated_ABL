import numpy as np
class BaysianSceneGenerator:

    def __init__(self, baysianNetwork):
        self.network = baysianNetwork
        self.generate_scenario()

    def generate_list_scenario(self):
        self.generate_scenario()
        return self.to_1D_Array(self.scenario)
    
    def to_1D_Array(self, scenario):
        array = []
        for comb in scenario:
            for feature in comb:
                array.append(feature)
        return array

    def generate_scenario(self):
        self.scenario_generator(6)
    
    @staticmethod
    def rand_zero_one_vector(n):
        arr = np.zeros(n)
        k = np.random.randint(n - n/4, n)
        arr[:k] = 1
        np.random.shuffle(arr)
        return arr
    
    def scenario_generator(self, num):
        scenario = []
        """
        locations = self.rand_zero_one_vector(num)
        for loc in locations:
            if loc == 0:
                col_con = []
                for _ in range(len(self.network.nodes) - 1):
                    col_con.append(-1)
                scenario.append(col_con)
            else:
        """
        column = list(self.network.generateState())
        self.best_recovery_behavior = column.pop()
        column = [column[idx] + idx * 2 for idx in range(len(column))]
        scenario.append(column)
        self.scenario = scenario
