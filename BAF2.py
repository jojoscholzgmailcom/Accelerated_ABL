"""
Created on Thursday Oct 13 2020
@author: Hamed Ayoobi
َAll rights reserved 2020
"""

"""
Modified by Jonas Scholz
"""

import itertools
import numpy as np
import operator
import ast
import random


class BAF2:
    support_weights = {}
    combination_feature_weights = {}
    subsets = []
    recovery_behaviors = []
    support_repetitions = {}
    sum_of_weights_for_each_recovery_behavior = {}
    current_best_recovery_behavior = "Nothing"
    negative_sets = []
    init_phase = True

    def __init__(self, featureDimensions):
        self.support_weights = {}
        self.combination_feature_weights = {}
        self.subsets = []
        self.recovery_behaviors = []
        self.support_repetitions = {}
        self.sum_of_weights_for_each_recovery_behavior = {}
        self.current_best_recovery_behavior = 0
        self.init_phase=True
        self.featureDimensions = featureDimensions
        self.numFeatures = len(self.featureDimensions)
        # self.recur_subset_for_comb(range(len(scenario) * 2))
        # for itr in self.subsets:
        #     self.combination_feature_weights[str(itr)] = 1

    def recur_subset(self, s, l=None):
        if l is None:
            l = len(s)
            self.subsets = []
        if 0 < l <= self.num_features_to_consider:
            for x in itertools.combinations(s, l):
                numbers = self.arg_to_combination_numbers(x)
                #print("New: ", numbers)
                # if str(numbers) not in self.negative_sets:
                if self.init_phase or (str(numbers) in self.combination_feature_weights):#(str(numbers) == max(self.combination_feature_weights.items(), key=operator.itemgetter(1))[0]):#(str(numbers) in self.combination_feature_weights):
                    if len(numbers) == self.num_features_to_consider:
                        try:
                            self.subsets.append(list(x))
                        except:
                            pass
            self.recur_subset(s, l - 1)
        if l > self.num_features_to_consider:
            self.recur_subset(s, l - 1)

    num_features_to_consider = 1

    def recur_subset_for_comb(self, s, l=None):
        if l is None:
            l = len(s)
            self.subsets = []
        if l > 0:
            for x in itertools.combinations(s, l):
                if len(x) == self.num_features_to_consider:
                    self.subsets.append(list(x))
            self.recur_subset_for_comb(s, l - 1)

    def arg_to_combination_numbers(self, argument1):
        lst = []
        for arg in argument1:
            # Change this number and the one below
            if len(arg) >= 3:
                for idx in range(self.numFeatures):
                    lst.append(arg[0] * self.numFeatures + idx)
            elif len(arg) == 2:
                # TODO: Figure out this number prob not 4
                lst.append(arg[0] * self.numFeatures + self.get_offset(arg[1]))
        return lst
    
    def get_offset(self, argNum):
        offset = 0
        sum = 0
        for num in self.featureDimensions:
            sum += num
            if argNum < sum:
                return offset
            offset += 1
        return offset - 1

    # Not sure how to change this
    def enumerate_scenarios(self, scenario):
        enumerated_scenarios = []
        for idx in range(len(scenario)):
            if scenario[idx][0] != -1:
                for featIdx in range(len(scenario[idx])):
                    enumerated_scenarios.append([idx, scenario[idx][featIdx]])
            else:
                enum_scenario = [idx]
                for featIdx in range(len(scenario[idx])):
                    enum_scenario.append(scenario[idx][featIdx])
                enumerated_scenarios.append(enum_scenario)
        return enumerated_scenarios

    def remove_others(self, idx):
        for subset in self.subsets[idx:]:
            numbers = self.arg_to_combination_numbers(subset)
            self.combination_feature_weights.pop(str(numbers), None)

    def compute_combination_feature_weights(self, best_recovery_behavior, all_scenarios_so_far,
                                            corresponding_recoveries_for_scenarios_so_far):
        should_change = True
        
        # self.combination_feature_weights = {}
        if len(all_scenarios_so_far) > 0:
            self.init_phase = False
            for idx, subset in enumerate(self.subsets):
                numbers = self.arg_to_combination_numbers(subset)
                selected_columns_with_recovery = np.zeros((len(all_scenarios_so_far), len(numbers) + 1))
                selected_columns_with_recovery[:, np.arange(len(numbers))] = np.array(all_scenarios_so_far)[:, numbers]
                selected_columns_with_recovery[:, -1] = corresponding_recoveries_for_scenarios_so_far
                unique_selected_columns_with_recovery = np.unique(selected_columns_with_recovery, axis=0)
                positive = len(selected_columns_with_recovery) - len(unique_selected_columns_with_recovery)
                unique_selected_columns_without_recovery = np.unique(selected_columns_with_recovery[:, :-1], axis=0)
                negative = len(unique_selected_columns_with_recovery) - len(unique_selected_columns_without_recovery)

                # current_scnerio_selected_columns = numerical_scenario[numbers].astype('float64')
                overal = positive + 1 + negative * (-50)

                if negative <= 0:
                    should_change = False
                    self.combination_feature_weights[str(numbers)] = overal
                    # self.remove_others(idx)
                    # return should_change
                else:
                    self.combination_feature_weights.pop(str(numbers), None)
        else:
            should_change = False
        return should_change

    def prune_combination_feature_weights(self):
        if self.combination_feature_weights != {}:
            max_val = max(v for k, v in self.combination_feature_weights.items())
            self.combination_feature_weights = dict((k, v) for k, v in self.combination_feature_weights.items() if v > max(0, max_val - 10))
        else:
            self.init_phase = True

    def update_baf(self, scenario, best_recovery_behavior, all_scenarios_so_far,
                   corresponding_recoveries_for_scenarios_so_far):
        self.current_best_recovery_behavior = best_recovery_behavior
        enumerated_scenarios = self.enumerate_scenarios(self.to_2D_array(scenario))
        self.recur_subset(enumerated_scenarios)
        self.add_recovery_behavior()
        if self.compute_combination_feature_weights(best_recovery_behavior, all_scenarios_so_far,
                                                    corresponding_recoveries_for_scenarios_so_far):
            #print("Test more feature (new)")
            self.num_features_to_consider += 1
            self.negative_sets = []
            self.init_phase = True

    def divid_noc_in_scenario(self, scenario):
        divided_noc_scenario = []
        for state in scenario:
            if (len(state)>=3):
                for idx in range(len(state) - 1):
                    divided_noc_scenario.append([state[0], state[idx + 1]])
            else:
                divided_noc_scenario.append(state)
        return divided_noc_scenario

    def add_recovery_behavior(self):
        if self.current_best_recovery_behavior not in self.recovery_behaviors:
            self.recovery_behaviors.append(self.current_best_recovery_behavior)

    def most_common(self,lst):
        return max(set(lst), key=lst.count)

    def compute_sum_of_weights_for_each_recovery_behavior(self, show_rule, scenario, previous_scenarios,
                                                          previous_best_recoveries, num_scenario):
        if self.combination_feature_weights == {}:
            return ''
        sum_of_weights = {}
        max_support_for_recovery_behavior = {}
        self.sum_of_weights_for_each_recovery_behavior = sum_of_weights
        max_weighted_combinations_key = ""
        max_weighted_combinations_value = -10000
        for key, value in self.combination_feature_weights.items():
            if value > max_weighted_combinations_value:
                max_weighted_combinations_value = value
                max_weighted_combinations_key = key
        max_indices_list = max_weighted_combinations_key.split('[')[1].split(']')[0].split(',')
        max_indices_list = list(map(int, max_indices_list))
        # Not 100% sure if scenario is correct here
        current_scenarios_columns = list(np.array(num_scenario)[max_indices_list])
        recovery_behavior_weights = {}
        for recovery_behavior in self.recovery_behaviors:
            recovery_behavior_weights[recovery_behavior] = 0
        for recovery_behavior in self.recovery_behaviors:
            rec_beh_num = recovery_behavior
            for idx, prev_scenario in enumerate(previous_scenarios):
                if (rec_beh_num == previous_best_recoveries[idx]) and (
                        str(current_scenarios_columns) == str(list(np.array(prev_scenario)[max_indices_list]))): # this lines checks whether a previous scenario have the same recovery behavior as the current one or not and also using the feature numbers extracted from the highest combination weight
                    recovery_behavior_weights[previous_best_recoveries[idx]] += 1
        scenario = self.divid_noc_in_scenario(scenario)
        if recovery_behavior_weights != {}:
            max_val = max([v for k,v in recovery_behavior_weights.items()])
            max_behaviors = [k for k,v in recovery_behavior_weights.items() if v==max_val]
            if len(max_behaviors) == 1:
                predicted_recovery = max(recovery_behavior_weights.items(), key=operator.itemgetter(1))[0]
                if show_rule:
                    print(f"{[scenario[idx] for idx in max_indices_list]}->{predicted_recovery} -- weight: {recovery_behavior_weights[predicted_recovery]}")
                return predicted_recovery
            else:
                return self.most_common(previous_best_recoveries)

        else:
            return ''


    def find_recovery_behavior_with_highest_sum_of_support(self):
        max = -10000
        recovery_behavior_with_highest_sum = ""
        for recovery_behavior, sum_weight in self.sum_of_weights_for_each_recovery_behavior.items():
            if sum_weight > max:
                max = sum_weight
                recovery_behavior_with_highest_sum = recovery_behavior
        return recovery_behavior_with_highest_sum

    def to_1D_array(self, scenario):
        array = []
        for comb in scenario:
            for feature in comb:
                array.append(feature)
        return array
    
    def to_2D_array(self, scenario_1D):
        return [scenario_1D[i:i + self.numFeatures] for i in range(0, len(scenario_1D), self.numFeatures)]

    def generate_second_guess(self, scenario, previous_scenarios, previous_best_recoveries, show_rule=True):
        scenario_2D = self.to_2D_array(scenario)
        enumerated_scenarios = self.enumerate_scenarios(scenario_2D)
        self.recur_subset(enumerated_scenarios)
        return self.compute_sum_of_weights_for_each_recovery_behavior(show_rule, enumerated_scenarios, previous_scenarios,
                                                                      previous_best_recoveries, scenario)
