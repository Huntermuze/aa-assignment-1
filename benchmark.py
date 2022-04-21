import math
import sys
import timeit
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import random
from axis_pair import AxisPair
from dictionary.word_frequency import WordFrequency
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary


def usage():
    """
    Print help/usage message.
    """
    print('python3 benchmark.py', '<approach>')
    print('<approach> = <list | hashtable | tst | all>')
    sys.exit(1)


def execute_commands(argument, input_sizes, command, num_commands):
    #word_freq_to_add = get_command_arguments(command)
    times = []

    for (i, n) in enumerate(input_sizes):
        agents = get_agents(argument)
        word_freq_to_add = get_command_random(command, get_word_freq_list(n), n, num_commands)

        for (j, agent) in enumerate(agents):
            avg = 0

            agent.build_dictionary(get_word_freq_list(n))

            if command == 'S':
                for x in word_freq_to_add:
                    avg += timeit.timeit(lambda: agent.search(x), number=1) * 1000 * 1000 * 1000
            elif command == 'A':
                for x in word_freq_to_add:
                    avg += timeit.timeit(lambda: agent.add_word_frequency(x), number=1) * 1000 * 1000 * 1000
            elif command == 'D':
                for x in word_freq_to_add:
                    avg += timeit.timeit(lambda: agent.delete_word(x), number=1) * 1000 * 1000 * 1000
            elif command == 'AC':
                for x in word_freq_to_add:
                    avg += timeit.timeit(lambda: agent.autocomplete(x), number=1) * 1000 * 1000 * 1000

            num_commands = len(word_freq_to_add)
            times.append(math.log(avg / num_commands, 10))
            print("AGENT [" + str(j + 1) + "] > " + "Time " + str(i + 1) + ": " + str(times[i + j]))

    return times

def get_command_random(command, input_file, n, num_commands):
    words_frequencies_from_file = []
    # scenario 1 grow
    if command == 'A':
        if n == '50':
            max_num = 50
        elif n == '500':
            max_num = 500
        elif n == '1k':
            max_num = 1000
        elif n == '2k':
            max_num = 2000
        elif n == '5k':
            max_num = 5000
        elif n == '10k':
            max_num = 10000
        elif n == '50k':
            max_num = 50000
        elif n == '100k':
            max_num = 100000
        for i in range(0, num_commands):
            store_max = i
            words_frequencies_from_file.append(input_file[random.randint(0, max_num-1)])
        print("The max num is: " + str(store_max + 1))
        return words_frequencies_from_file
    # scenario 2 shrink + scenario 3 search
    elif command == 'D' or command == 'S':
        if n == '50':
            max_num = 50
        elif n == '500':
            max_num = 500
        elif n == '1k':
            max_num = 1000
        elif n == '2k':
            max_num = 2000
        elif n == '5k':
            max_num = 5000
        elif n == '10k':
            max_num = 10000
        elif n == '50k':
            max_num = 50000
        elif n == '100k':
            max_num = 100000
        for i in range(0, 1000):
            store_max = i
            words_frequencies_from_file.append(input_file[random.randint(0, max_num-1)].word)
        print("The max num is: " + str(store_max + 1))
        return words_frequencies_from_file
    #scenario 3 autocomplete
    elif command == 'AC':
        data_file = open("commands/20_commands_autocomplete", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            words_frequencies_from_file.append(word)
        data_file.close()
        return words_frequencies_from_file


def get_command_arguments(command):
    words_frequencies_from_file = []
    # scenario 1
    if command == 'A':
        data_file = open("commands/20_commands_add", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            frequency = int(values[1])
            word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
            words_frequencies_from_file.append(word_frequency)
        data_file.close()
        return words_frequencies_from_file
    # scenario 2
    elif command == 'D':
        data_file = open("commands/20_commands_delete", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            words_frequencies_from_file.append(word)
        data_file.close()
        return words_frequencies_from_file
    # scenario 3
    elif command == 'S':
        data_file = open("commands/20_commands_search", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            words_frequencies_from_file.append(word)
        data_file.close()
        return words_frequencies_from_file
    elif command == 'AC':
        data_file = open("commands/20_commands_autocomplete", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            words_frequencies_from_file.append(word)
        data_file.close()
        return words_frequencies_from_file


def get_word_freq_list(n):
    words_frequencies_from_file = []
    data_file = open("input/input_" + n, 'r')
    for line in data_file:
        values = line.split()
        word = values[0]
        frequency = int(values[1])
        word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
        words_frequencies_from_file.append(word_frequency)
    data_file.close()
    return words_frequencies_from_file


def final_analysis(argument, input_sizes, command):
    num_commands = 1000
    total_times = []
    axes = []
    upper_bound = 10

    for iteration in range(0, upper_bound):
        total_times.append(execute_commands(argument, input_sizes, command, num_commands))

    # Contains the times for the list dictionary, hashtable dictionary and the tst dictionary, respectively.
    all_dictionaries = [[], [], []]
    for run in total_times:
        if argument == "all":
            all_dictionaries[0].append(run[0::3])
            all_dictionaries[1].append(run[1::3])
            all_dictionaries[2].append(run[2::3])
        elif argument == "list":
            all_dictionaries[0].append(run)
        elif argument == "hashtable":
            all_dictionaries[1].append(run)
        else:
            all_dictionaries[2].append(run)

    if len(all_dictionaries[0]) > 0:
        axes.append(AxisPair(input_sizes, np.average(np.array(all_dictionaries[0]), axis=0)))
    if len(all_dictionaries[1]) > 0:
        axes.append(AxisPair(input_sizes, np.average(np.array(all_dictionaries[1]), axis=0)))
    if len(all_dictionaries[2]) > 0:
        axes.append(AxisPair(input_sizes, np.average(np.array(all_dictionaries[2]), axis=0)))

    # numeric_input_sizes = np.array([50, 500, 1000, 2000, 5000, 10000, 50000, 100000])
    # x = np.linspace(numeric_input_sizes.min(), numeric_input_sizes.max(), 300)
    #
    # spl = make_interp_spline(numeric_input_sizes, times, k=3)
    # graph_smooth = spl(x)
    # plot_graph([AxisPair(x, graph_smooth)])

    plot_graph(axes, input_sizes[0], input_sizes[-1], command, num_commands)


def plot_graph(axes, x_axis_min, x_axis_max, command, num_commands):
    graph_title = ''
    if len(axes) > 0:
        for idx, axes_pair in enumerate(axes):
            title = "List"

            if idx == 1:
                title = "Hashtable"
            elif idx == 2:
                title = "TST"

            plt.plot(axes_pair.x_axis, axes_pair.y_axis, label=title)
    else:
        return

    if command == 'S':
        graph_title = 'Search Benchmark'
    elif command == 'A':
        graph_title = 'Add Benchmark'
    elif command == 'D':
        graph_title = 'Delete Benchmark'
    elif command == 'AC':
        graph_title = 'Autocomplete Benchmark'

    plt.xlabel('Number of Elements before Operation')
    plt.xlim(x_axis_min, x_axis_max)
    plt.ylabel('Log of Time per ' + str(num_commands) + ' Operations (ns)')
    plt.title(graph_title)
    plt.legend(loc="upper left")
    plt.show()


def get_agents(argument):
    if argument == 'list':
        return [ListDictionary()]
    elif argument == 'hashtable':
        return [HashTableDictionary()]
    elif argument == 'tst':
        return [TernarySearchTreeDictionary()]
    elif argument == 'all':
        return [ListDictionary(), HashTableDictionary(), TernarySearchTreeDictionary()]
    else:
        print('Incorrect argument value.')
        usage()


if __name__ == '__main__':
    input_sizes_grow = ['50', '500', '1k', '2k', '5k', '10k', '50k', '100k']
    input_sizes_shrink = ['100k', '50k', '10k', '5k', '2k', '1k', '500', '50']

    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 2:
        print('Incorrect number of arguments.')
        usage()

    # search
    command = input("Please enter a command (S, A, D, AC): ")
    if command == 'S' or command == 'A' or command == 'D' or command == 'AC':
        final_analysis(args[1], input_sizes_grow, command)
    else:
        print('Unknown command.')
