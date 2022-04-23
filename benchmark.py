import math
import sys
import timeit
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import List
from axis_pair import AxisPair
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary

n_mapped_to_int = {'50': 50, '500': 500, '1k': 1000, '2k': 2000, '5k': 5000, '10k': 10000, '50k': 50000, '100k': 100000}
input_sizes = ['50', '500', '1k', '2k', '5k', '10k', '50k', '100k']
cached_input_from_file = {}


def main():
    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 2:
        print('Incorrect number of arguments.')
        usage()

    # search
    command = input("Please enter a command (S, A, D, AC): ")
    if command == 'S' or command == 'A' or command == 'D' or command == 'AC':
        final_analysis(args[1], command)
    else:
        print('Unknown command.')


def usage():
    """
    Print help/usage message.
    """
    print('python3 benchmark.py', '<approach>')
    print('<approach> = <list | hashtable | tst | all>')
    sys.exit(1)


def final_analysis(agent_type: str, command: str):
    adds_to_choose_from = get_input_from_file("input/input_adds", True)
    num_commands = 1000
    upper_bound = 10
    total_times = []
    axes = []
    approaches = ["List", "Hashtable", "TST"]
    speeds = []
    get_graph_input = input("Enter the type of graph you want (speed or size): ")

    # Reverse the input_size if we are dealing with a delete command.
    if command == 'D':
        input_sizes.reverse()

    for iteration in range(0, upper_bound):
        total_times.append(execute_commands(agent_type, command, num_commands, adds_to_choose_from))

    # Contains the times for the list dictionary, hashtable dictionary and the tst dictionary, respectively.
    all_dictionaries = [[], [], []]
    for run in total_times:
        if agent_type == "all":
            all_dictionaries[0].append(run[0::3])
            all_dictionaries[1].append(run[1::3])
            all_dictionaries[2].append(run[2::3])
        elif agent_type == "list":
            all_dictionaries[0].append(run)
        elif agent_type == "hashtable":
            all_dictionaries[1].append(run)
        else:
            all_dictionaries[2].append(run)
    for dictionary_time in all_dictionaries:
        if len(dictionary_time) > 0:
            if get_graph_input == "size":
                axes.append(AxisPair(input_sizes, np.average(np.array(dictionary_time), axis=0)))
            elif get_graph_input == "speed":
                speeds.append(np.average(np.average(np.array(dictionary_time), axis=0)))

    plot_graph(axes, input_sizes[0], input_sizes[-1], command, num_commands, get_graph_input, approaches, speeds)


def execute_commands(agent_type: str, command: str, num_commands: int,
                     adds_to_choose_from: List[WordFrequency]) -> list:
    times = []

    for (i, n) in enumerate(input_sizes):
        agents = get_agents(agent_type)
        word_freqs_to_process = get_command_random(command, get_input_from_file("input/input_" + n, True), n, num_commands,
                                               adds_to_choose_from)

        for (j, agent) in enumerate(agents):
            avg = 0
            agent.build_dictionary(get_input_from_file("input/input_" + n, True))

            if command == 'S':
                method_to_time = agent.search
            elif command == 'A':
                method_to_time = agent.add_word_frequency
            elif command == 'D':
                method_to_time = agent.delete_word
            else:
                method_to_time = agent.autocomplete

            for x in word_freqs_to_process:
                avg += timeit.timeit(lambda: method_to_time(x), number=1) * 1000 * 1000 * 1000

            times.append(math.log(avg / num_commands, 10))
            print("AGENT [" + str(j + 1) + "] > " + n + " Size Time" + ": " + str(times[i + j]))

    return times


def get_agents(agent_type: str) -> List[BaseDictionary]:
    if agent_type == 'list':
        return [ListDictionary()]
    elif agent_type == 'hashtable':
        return [HashTableDictionary()]
    elif agent_type == 'tst':
        return [TernarySearchTreeDictionary()]
    elif agent_type == 'all':
        return [ListDictionary(), HashTableDictionary(), TernarySearchTreeDictionary()]
    else:
        print('Incorrect argument value.')
        usage()


def get_input_from_file(file_path: str, create_word_frequency: bool) -> list:
    input_size = file_path[12:]

    if input_size not in cached_input_from_file:
        input_from_file = []

        with open(file_path, 'r') as data_file:
            for line in data_file:
                values = line.split()
                word = values[0]

                # If each line contains a word and its frequency
                if create_word_frequency:
                    frequency = int(values[1])
                    input_from_file.append(WordFrequency(word, frequency))
                # If there is only a word and no frequency (i.e., delete, search or autocomplete commands).
                else:
                    input_from_file.append(word)

        # Add to the cached input list to speedup the benchmarking.
        cached_input_from_file[input_size] = input_from_file

    return cached_input_from_file[input_size]


def get_command_random(command: str, word_frequencies_from_file: List[WordFrequency], n: str,
                       num_commands: int, adds_to_choose_from: List[WordFrequency]) -> list:
    command_input = []
    max_num = n_mapped_to_int[n]

    # Scenario 1 grow
    if command == 'A':
        max_adds = len(adds_to_choose_from)
        for i in range(0, num_commands):
            command_input.append(adds_to_choose_from[random.randint(0, max_adds - 1)])
    # Scenario 2 shrink + Scenario 3 search
    elif command == 'D' or command == 'S':
        for i in range(0, num_commands):
            command_input.append(word_frequencies_from_file[random.randint(0, max_num - 1)].word)
    # Scenario 3 autocomplete
    else:
        for i in range(0, num_commands):
            picked_word = word_frequencies_from_file[random.randint(0, max_num - 1)].word
            if len(picked_word) <= 4:
                cur_ac = len(picked_word)
            else:
                cur_ac = 5
            command_input.append(picked_word[0:random.randint(1, cur_ac)])

    return command_input


def plot_graph(axes: List[AxisPair], x_axis_min: str, x_axis_max: str, command: str, num_commands: int, graph_input: str, approaches, speeds):
    #if len(axes) <= 0:
        #return

    if graph_input == "size":
        for idx, axes_pair in enumerate(axes):
            title = "List"

            if idx == 1:
                title = "Hashtable"
            elif idx == 2:
                title = "TST"

            plt.plot(axes_pair.x_axis, axes_pair.y_axis, label=title)

        if command == 'S':
            graph_title = 'Search Benchmark'
        elif command == 'A':
            graph_title = 'Add Benchmark'
        elif command == 'D':
            graph_title = 'Delete Benchmark'
        else:
            graph_title = 'Autocomplete Benchmark'

        plt.xlabel('Number of Elements before Operation')
        plt.xlim(x_axis_min, x_axis_max)
        plt.ylabel('Log of Time per ' + str(num_commands) + ' Operations (ns)')
        plt.title(graph_title)
        plt.legend(loc="upper left")
        plt.show()
    
    elif graph_input == "speed":
        plt.bar(approaches, speeds)
        plt.show()
        print(speeds[0])
        print(speeds[1])
        print(speeds[2])


if __name__ == '__main__':
    main()
