"""
Created on Thursday Oct 13 2020
@author: Hamed Ayoobi
َAll rights reserved 2020
"""

import itertools
import numpy as np
import operator
import ast



class BAF:
    arguments = []
    attacks = []
    supports = []
    support_weights = {}
    large_subsets = []
    subsets = []
    current_best_recovery_behavior = "Nothing"
    recovery_behaviors = []
    sum_of_weights_for_each_recovery_behavior = {}
    features_weights_for_each_recovery_behavior = []
    combination_feature_weights = {}
    feature_weights = {}
    show_rule = False

    def __init__(self, scenario):
        self.arguments = []
        self.attacks = []
        self.supports = []
        self.support_weights = {}
        self.large_subsets = []
        self.current_best_recovery_behavior = "Nothing"
        self.recovery_behaviors = []
        self.sum_of_weights_for_each_recovery_behavior = {}
        self.make_feature_weight_lists(scenario)
        self.recur_subset_for_comb(range(len(scenario) * 2))
        for itr in self.subsets:
            self.combination_feature_weights[str(itr)] = 1
        for i in range(len(scenario) * 2):
            self.feature_weights[i] = 0
        self.subsets = []

    def update_baf(self, scenario, best_recovery_behavior):
        self.current_best_recovery_behavior = best_recovery_behavior
        self.add_recovery_behavior()
        self.add_argument(best_recovery_behavior)
        self.add_arguments_from_scenario(scenario)

    def make_feature_weight_lists(self, scenario):
        if self.features_weights_for_each_recovery_behavior == []:
            self.features_weights_for_each_recovery_behavior = np.zeros(len(scenario) * 2)

    def add_recovery_behavior(self):
        if self.current_best_recovery_behavior not in self.recovery_behaviors:
            self.recovery_behaviors.append(self.current_best_recovery_behavior)
            self.add_bidirectional_attack_between_recovery_behaviors()

    def add_bidirectional_attack_between_recovery_behaviors(self):
        for recovery_behavior in self.recovery_behaviors:
            if recovery_behavior != self.current_best_recovery_behavior:
                self.add_attack(self.current_best_recovery_behavior, recovery_behavior)
                self.add_attack(recovery_behavior, self.current_best_recovery_behavior)

    num_features_to_consider = 4
    def recur_subset(self, s, l=None):
        if l is None:
            l = len(s)
            self.subsets = []
        if 0 < l <= self.num_features_to_consider:
            for x in itertools.combinations(s, l):
                if len(x) <= self.num_features_to_consider:
                    numbers = self.arg_to_combination_numbers(x)
                    try:
                        a = self.combination_feature_weights[str(numbers)]
                        self.subsets.append(list(x))
                    except:
                        pass
            self.recur_subset(s, l - 1)
        if l > self.num_features_to_consider:
            self.recur_subset(s, l - 1)

    # def recur_subset(self, s, l = None):
    #     if l is None:
    #         l = len(s)
    #         self.subsets = []
    #     if l > 0:
    #         for x in itertools.combinations(s, l):
    #             if len(x) <= self.num_features_to_consider:
    #                 numbers = self.arg_to_combination_numbers(x)
    #                 try:
    #                     a = self.combination_feature_weights[str(numbers)]
    #                     self.subsets.append(list(x))
    #                 except:
    #                     pass
    #         self.recur_subset(s, l - 1)

    def recur_subset_for_comb(self, s, l = None):
        if l is None:
            l = len(s)
            self.subsets = []
        if l > 0:
            for x in itertools.combinations(s, l):
                if len(x) <= self.num_features_to_consider:
                    self.subsets.append(list(x))
            self.recur_subset_for_comb(s, l - 1)

    def add_arguments_from_scenario(self, scenario):
        enumerated_scenarios = self.enumeratea_scenarios(scenario)
        self.recur_subset(enumerated_scenarios)
        for subset in self.subsets:
            self.add_argument(subset)
            self.add_support(subset, self.current_best_recovery_behavior)

    def enumeratea_scenarios(self,scenario):
        enumerated_scenarios = []
        for idx in range(len(scenario)):
            if scenario[idx][0] != 'Noc':
                enumerated_scenarios.append([idx, scenario[idx][0]])
                enumerated_scenarios.append([idx, scenario[idx][1]])
            else:
                enumerated_scenarios.append([idx, scenario[idx][0], scenario[idx][1]])
        return enumerated_scenarios

    def extract_arguments_from_scenario(self, scenario):
        enumerated_scenarios = self.enumeratea_scenarios(scenario)
        self.recur_subset(enumerated_scenarios)

    def compute_sum_of_weights_for_each_recovery_behavior(self, show_rule):
        sum_of_weights = {}
        max_support_for_recovery_behavior = {}
        self.sum_of_weights_for_each_recovery_behavior = sum_of_weights
        for subset in self.subsets:
            sbt = self.arg_to_combination_numbers(subset)
            if len(sbt) <=self.num_features_to_consider:
                for recovery_behavior in self.recovery_behaviors:
                    support_relation = f"{subset}->{recovery_behavior}"
                    comb_weight = 0
                    try:
                        comb_weight = self.combination_feature_weights[str(sbt)]
                    except:
                        comb_weight = 0
                    if (recovery_behavior in sum_of_weights) and (support_relation in self.support_weights):
                        # sum_of_weights[recovery_behavior] += self.support_weights[support_relation] * (self.combination_feature_weights[str(sbt)])
                        if (self.support_weights[support_relation] * comb_weight) > sum_of_weights[recovery_behavior]:
                            max_support_for_recovery_behavior[recovery_behavior] = support_relation
                        sum_of_weights[recovery_behavior] = max(self.support_weights[support_relation] * (comb_weight),
                                                                sum_of_weights[recovery_behavior])
                    elif support_relation in self.support_weights:
                        sum_of_weights[recovery_behavior] = self.support_weights[support_relation] * (comb_weight)
                        max_support_for_recovery_behavior[recovery_behavior] = support_relation
                    elif recovery_behavior in sum_of_weights:
                        pass
                    else:
                        sum_of_weights[recovery_behavior] = -1000

        self.sum_of_weights_for_each_recovery_behavior = sum_of_weights

        if show_rule:
            #show which rule has been used for finding the best recovery behavior at each step
            if self.sum_of_weights_for_each_recovery_behavior != {} and max_support_for_recovery_behavior != {}:
                max_key = max(self.sum_of_weights_for_each_recovery_behavior.items(), key=operator.itemgetter(1))[0]
                print(max_support_for_recovery_behavior[max_key])


    def find_recovery_behavior_with_highest_sum_of_support(self):
        max = -10000
        recovery_behavior_with_highest_sum = ""
        for recovery_behavior, sum_weight in self.sum_of_weights_for_each_recovery_behavior.items():
            if sum_weight > max:
                max = sum_weight
                recovery_behavior_with_highest_sum = recovery_behavior

        return recovery_behavior_with_highest_sum


    def add_argument(self, argument):
        if argument not in self.arguments:
            self.arguments.append(argument)

    def add_attack(self, argument1, argument2):
        if [argument1, argument2] not in self.attacks:
            self.attacks.append([argument1, argument2])

    def add_support(self, argument1, argument2):
        if [argument1, argument2] not in self.supports:
            self.supports.append([argument1, argument2])
        self.update_support_weight(argument1, argument2)


    def arg_to_combination_numbers(self, argument1):
        lst = []
        for arg in argument1:
            if len(arg)==3:
                lst.append(arg[0]*2)
                lst.append(arg[0]*2 + 1)
            elif len(arg) ==2:
                if arg[1] in ['red', 'green', 'blue', 'yellow']:
                    lst.append(arg[0]*2)
                else:
                    lst.append(arg[0]*2 + 1)
        return lst
    def support_to_list(self,support):
        arg1_part = support.split('->')[0]
        arg1_part = ast.literal_eval(arg1_part)
        return arg1_part

    def remove_unused_weights(self):
        max_val = max(v for k, v in self.combination_feature_weights.items())
        print(f"max combination weight: {max_val}")
        zero_weight_list = list(k for k, v in self.combination_feature_weights.items() if v <= max(0, max_val - 6))
        self.combination_feature_weights = dict((k, v) for k, v in self.combination_feature_weights.items() if v > max(0, max_val - 6))
        new_support_weights = self.support_weights.copy()
        new_supports = []
        for (support, weight) in self.support_weights.items():
            support_list = self.support_to_list(support)
            feature_combs = self.arg_to_combination_numbers(support_list)
            if str(feature_combs) in zero_weight_list and weight <= 1:
                del new_support_weights[support]
        self.support_weights = new_support_weights
        del_support_ix_list = []
        for idx, [arg1, arg2] in enumerate(self.supports):
            feature_combs = self.arg_to_combination_numbers(arg1)
            if str(feature_combs) in zero_weight_list:
                pass
            else:
                new_supports.append([arg1, arg2])
        self.supports = new_supports

        new_args = []
        for arg1 in self.arguments:
            if arg1 not in self.recovery_behaviors:
                feature_combs = self.arg_to_combination_numbers(arg1)
                if str(feature_combs) in zero_weight_list:
                    pass
                else:
                    new_args.append(arg1)
            else:
                new_args.append(arg1)
        self.arguments = new_args


    def add_weight_of_all_supersets(self, args_set, inc_step):
        for (key, value) in self.combination_feature_weights.items():
            if args_set != key:
                contain_all = True
                for arg in args_set:
                    if str(arg) not in key:
                        contain_all = False
                        break
                if contain_all:
                    self.combination_feature_weights[key] += 1

    def decrease_weight_of_all_supersets(self, args_set, inc_step):
        for (key, value) in self.combination_feature_weights.items():
            if args_set != key:
                contain_all = True
                for arg in args_set:
                    if str(arg) not in key:
                        contain_all = False
                        break
                if contain_all:
                    self.combination_feature_weights[key] -= 1


    def update_support_weight(self, argument1, argument2,):
        args_set = self.arg_to_combination_numbers(argument1)
        if len(args_set) <= self.num_features_to_consider:
            inc_step = 1
            if (f"{argument1}->{argument2}" in self.support_weights):
                try:
                    self.combination_feature_weights[str(args_set)] += inc_step
                    # self.add_weight_of_all_supersets(args_set, inc_step)
                except:
                    self.combination_feature_weights[str(args_set)] = inc_step
                # self.support_weights[f"{argument1}->{argument2}"] += 0.1
                for arg in args_set:
                    self.feature_weights[arg] += 1


            repetitions = {}
            sum = 1
            for recovery_behavior in self.recovery_behaviors:
                if recovery_behavior != argument2:
                    if f"{argument1}->{recovery_behavior}" in self.support_weights:
                        repetitions[recovery_behavior] = 1
                        sum += 1
                        try:
                            self.combination_feature_weights[str(args_set)] -= 50
                            # self.decrease_weight_of_all_supersets(args_set, inc_step)
                        except:
                            self.combination_feature_weights[str(args_set)] = 0
                        for arg in args_set:
                            self.feature_weights[arg] -= 1

            self.support_weights[f"{argument1}->{argument2}"] = 1 / float(sum) #if sum == 1 else 0
            for recovery_behavior, repetition in repetitions.items():
                if repetition == 1:
                    self.support_weights[f"{argument1}->{recovery_behavior}"] = 1 / float(sum) #if sum == 1 else 0

    def generate_second_guess(self, scenario, show_rule=False):
        self.extract_arguments_from_scenario(scenario)
        self.compute_sum_of_weights_for_each_recovery_behavior(show_rule)
        return self.find_recovery_behavior_with_highest_sum_of_support()

