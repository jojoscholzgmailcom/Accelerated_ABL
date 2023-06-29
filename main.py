import BAF2
from BaysianSceneGenerator import BaysianSceneGenerator
from generateBN import DependenciesSingleLayer
from generateGeneralBN import DependenciesMultiLayer
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from configurationsBN import ConfigurationBN
from sampling import *
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import csv
import bnlearn as bn
import pandas as pd
from timeit import default_timer as timer

max_time_per_iteration = 60 * 6

def run_multiple_iterations(comb, iterations, configurations: ConfigurationBN, numAttempts, all_TPs, all_DT_TPs, end_confusion_matrix, times) -> None:
    net = configurations.createBayesianNetwork()
    print(configurations.numNodes)
    #net.showNetwork()
    gen = BaysianSceneGenerator(net)
    for iterIdx in range(iterations):
        run_single_iteration(comb, iterIdx, net, gen, configurations, numAttempts, all_TPs, all_DT_TPs, end_confusion_matrix, times)

def run_single_iteration(comb: int, itr: int, net: BayesianNetwork, gen: BaysianSceneGenerator, configurations: ConfigurationBN, number_of_attempts: int, all_TPs: np.array, all_DT_TPs: np.array, end_confusion_matrix, times):
    baf = BAF2.BAF2([2 for _ in range(configurations.numNodes)])
    saved_scenarios_in_memory_for_other_approaches = []
    #saved_scenarios = {}
    #saved_scenarios_df = pd.DataFrame(columns=[f"{i}" if i < len(net.nodes) - 1 else "decision" for i in range(len(net.nodes))])
    #for i in range(len(net.nodes) - 1):
    #    saved_scenarios[f"{i}"] = []
    #saved_scenarios['decision'] = []
    saved_best_recovery_behaviors_in_memory_for_other_approaches = []
    confusion_matrix = np.zeros((4))# TP FN FP TN
    #confusion_matrix_dt = np.zeros((4))# TP FN FP TN
    #confusion_matrix_nn = np.zeros((4))# TP FN FP TN
    TP = 0
    DT_TP = 0
    #feature_indices = []
    # time.sleep(10)
    start = timer()
    #saved_attempts_dt = []
    #saved_attempts_nn = []
    start_time = time.time()
    end_time = time.time() + max_time_per_iteration
    for attempt in range(number_of_attempts):
        start = timer()
        if end_time <= time.time():
            return
        scenario_list = gen.generate_list_scenario()
        #guess = baf.generate_second_guess(scenario_list, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, show_rule=True)
        #baf.update_baf(scenario_list, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches)
        #if gen.best_recovery_behavior == guess:
        #    if (guess % 2) == 1:
        #        confusion_matrix[0] += 1 #True Positive
        #    else:
        #        confusion_matrix[3] += 1 #True Negative
        #    TP += 1
        #else:
        #    if guess != None and guess != "":
        #        if (guess % 2) == 1:
        #            confusion_matrix[2] += 1 #False Positive
        #        else:
        #            confusion_matrix[1] += 1 #False Negative

        #Structure Learning (DOES NOT WORK!!!!)
        #if len(saved_scenarios_df.index) > 5:
        #    model = bn.structure_learning.fit(saved_scenarios_df, methodtype='ex', scoretype='bic')
        #    model = bn.independence_test(model, saved_scenarios_df, alpha=0.05, prune=False)
        #    copy_scenario_list = scenario_list
        #    copy_scenario_list.append(gen.best_recovery_behavior)
        #    new_scenario_df = pd.DataFrame(columns=[f"{i}" if i < len(net.nodes) - 1 else "decision" for i in range(len(net.nodes))])
        #    new_scenario_df.loc[len(new_scenario_df)] = copy_scenario_list
        #    print(new_scenario_df)
        #    print(model)
        #    output = bn.predict(model, new_scenario_df, variables=['decision'])
        #    print(output)
        #    guess = output['decision']
        #    if gen.best_recovery_behavior == guess:
        #        if (guess % 2) == 1:
        #            confusion_matrix[0] += 1 #True Positive
        #        else:
        #            confusion_matrix[3] += 1 #True Negative
        #        TP += 1
        #    else:
        #        if guess != None and guess != "":
        #            if (guess % 2) == 1:
        #                confusion_matrix[2] += 1 #False Positive
        #            else:
        #                confusion_matrix[1] += 1 #False Negative



        all_TPs[itr, attempt] = TP
        #Decision tree with sklearn
        if saved_scenarios_in_memory_for_other_approaches:
            #trainClassfier(tree.DecisionTreeClassifier(), scenario_list, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, None, confusion_matrix, itr, attempt, net)
            trainClassfier(MLPClassifier(solver='lbfgs', hidden_layer_sizes=(8,)), scenario_list, gen.best_recovery_behavior, saved_scenarios_in_memory_for_other_approaches, saved_best_recovery_behaviors_in_memory_for_other_approaches, None, confusion_matrix, itr, attempt, net)
            # tree.plot_tree(clf)
            # plt.show()
        
        #for i in range(len(net.nodes) - 1):
        #    saved_scenarios[f"{i}"].append(scenario_list[i])
        #saved_scenarios['decision'].append(gen.best_recovery_behavior)
        saved_scenarios_in_memory_for_other_approaches.append(scenario_list)
        saved_best_recovery_behaviors_in_memory_for_other_approaches.append(gen.best_recovery_behavior)
        #scenario_list.append(gen.best_recovery_behavior)
        #saved_scenarios_df.loc[len(saved_scenarios_df)] = scenario_list
        # if attempt == 0:
        #     time.sleep(10)
        # print(f"time: {timer()-start} s")
        print(f"{attempt}:Our: {TP}, Decision tree: {DT_TP}")

        #writeLine("attempt-results.csv", [configurations.type, comb, itr, attempt, net.numTotalDependencies(), len(net.nodes), net.numLastDependency(), (confusion_matrix[0] + confusion_matrix[3]) / (attempt + 1), confusion_matrix[0], confusion_matrix[1], confusion_matrix[2], confusion_matrix[3]])    
    #writeLines("attempt-results-dt.csv", saved_attempts_dt)
    #writeLines("attempt-results-nn.csv", saved_attempts_nn)
    end_confusion_matrix.append(confusion_matrix)
    one_iteration_time = timer() - start
    times.append(one_iteration_time)
    print("average_per_iteration_time: ", np.mean(times))
    print(f"Our model true positives: {TP}")
    print(f"Decision Tree's true positives: {DT_TP}")
    print(f"Overal: {np.mean(all_TPs[:itr+1],axis=0)}")
    print(f"Overal accuracy: {np.mean(all_TPs[:itr+1],axis=0)/(np.array(range(number_of_attempts)) + 1)}")
    print(f"Confusion Matrix: \n{confusion_matrix[0]}, {confusion_matrix[1]}\n{confusion_matrix[2]}, {confusion_matrix[3]}")
    #print(f"Confusion Matrix DT: \n{confusion_matrix_dt[0]}, {confusion_matrix_dt[1]}\n{confusion_matrix_dt[2]}, {confusion_matrix_dt[3]}")

    #print(f"Overal DT: {np.mean(all_DT_TPs,axis=0)}")
    #print(f"Overal DT accuracy: {np.mean(all_DT_TPs[:itr+1],axis=0)/(np.array(range(number_of_attempts)) + 1)}")
    writeLine("end-results.csv", [configurations.type, comb, itr, net.numTotalDependencies(), len(net.nodes), net.numLastDependency(), (confusion_matrix[0] + confusion_matrix[3]) / (number_of_attempts), confusion_matrix[0], confusion_matrix[1], confusion_matrix[2], confusion_matrix[3], time.time() - start_time])
    #ax.plot(range(number_of_attempts), np.mean(all_TPs[:itr+1], axis=0)/(np.array(range(number_of_attempts)) + 1), label=f"ABL ({numNodes})")

def trainClassfier(classifier, scenario_list, solution, saved_scenarios, saved_solutions, saved_attempts, confusion_matrix, itr, attempt, net):
    classifier = classifier.fit(saved_scenarios, saved_solutions)
    guess = classifier.predict([scenario_list])[0]
    if guess == solution:
        if (guess % 2) == 1:
            confusion_matrix[0] += 1 #True Positive
        else:
            confusion_matrix[3] += 1 #True Negative
    elif guess != None and guess != "":
        if (guess % 2) == 1:
            confusion_matrix[2] += 1 #False Positive
        else:
            confusion_matrix[1] += 1 #False Negative
    if saved_attempts != None:
        saved_attempts.append([configurations.type, comb, itr, attempt, net.numTotalDependencies(), len(net.nodes), net.numLastDependency(), (confusion_matrix[0] + confusion_matrix[3]) / (attempt), confusion_matrix[0], confusion_matrix[1], confusion_matrix[2], confusion_matrix[3]])


def writeColumnLables(filename: str, data: list):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def writeLine(filename: str, data: list):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def writeLines(filename: str, data: list):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == "__main__":
    number_of_attempts = 200
    number_of_iterations = 25
    all_TPs = np.zeros((number_of_iterations,number_of_attempts))# Check this out more
    all_DT_TPs = np.zeros((number_of_iterations, number_of_attempts))
    end_confusion_matrix = []
    start_time = time.process_time()
    times = []
    minNodes = 2
    maxNodes = 22
    configurations = ConfigurationBN(minNodes, maxNodes, 1, maxNodes + 1)
    #BayesianNetwork(DependenciesMultiLayer(10, 2, 2)).showNetwork()
    writeColumnLables("end-results.csv", ["type", "combination", "iteration", "totalDependencies", "totalNodes", "decisionDependencies", "accuracy", "truePositive", "falseNegative", "falsePositive", "trueNegative", "runtime"])
    writeColumnLables("attempt-results.csv", ["type", "combination", "iteration", "attempt", "totalDependencies", "totalNodes", "decisionDependencies", "accuracy", "truePositive", "falseNegative", "falsePositive", "trueNegative"])
    #writeColumnLables("attempt-results-dt.csv", ["type", "combination", "iteration", "attempt", "totalDependencies", "totalNodes", "decisionDependencies", "accuracy", "truePositive", "falseNegative", "falsePositive", "trueNegative"])
    #writeColumnLables("attempt-results-nn.csv", ["type", "combination", "iteration", "attempt", "totalDependencies", "totalNodes", "decisionDependencies", "accuracy", "truePositive", "falseNegative", "falsePositive", "trueNegative"])
    for comb in range(configurations.combinations):
        configurations.updateCombination()
        if configurations.type == 2:
            break
        run_multiple_iterations(comb, number_of_iterations, configurations, number_of_attempts, all_TPs, all_DT_TPs, end_confusion_matrix, times)
    print(f"Mean Process Time = {np.mean(times)}")
    end_time = time.process_time()
    print(f"Total Process Time = {end_time - start_time}")
    plt.show()


