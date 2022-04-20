import math
import sys
import timeit
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
from dictionary.node import Node
from AxisPair import AxisPair
from dictionary.word_frequency import WordFrequency
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary


def usage():
    """
    Print help/usage message.
    """
    print('python3 test_env.py', '<approach>')
    print('<approach> = <list | hashtable | tst | all>')
    sys.exit(1)


def execute_commands(argument, input_sizes, command):
    word_freq_to_add = get_command_arguments(command)
    times = []

    # Append a new sublist for each requested agent.
    for i in range(0, len(get_agents(argument))):
        times.append([])

    for (input_index, n) in enumerate(input_sizes):
        agents = get_agents(argument)

        for (index, agent) in enumerate(agents):
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

            times[index].append(math.log(avg / 1000, 10))
            print("AGENT [" + str(index + 1) + "] > " + "Time " + str(input_index + 1) + ": " + str(
                times[index][input_index]))

    return times

    # numeric_input_sizes = np.array([50, 500, 1000, 2000, 5000, 10000, 50000, 100000])
    # x = np.linspace(numeric_input_sizes.min(), numeric_input_sizes.max(), 300)
    #
    # spl = make_interp_spline(numeric_input_sizes, times, k=3)
    # graph_smooth = spl(x)
    # plot_graph([AxisPair(x, graph_smooth)])


def plot_graph(axes, x_axis_min, x_axis_max):
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

    plt.xlabel('Number of Elements')
    plt.xlim(x_axis_min, x_axis_max)
    plt.ylabel('Log of Time per Operation (ns)')
    plt.title('Benchmarking')
    plt.legend(loc="upper left")
    plt.show()


def get_command_arguments(command):
    words_frequencies_from_file = []
    # scenario 1
    if command == 'A':
        data_file = open("50_inputs_add", 'r')
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
        data_file = open("eight_inputs_delete", 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            words_frequencies_from_file.append(word)
        data_file.close()
        return words_frequencies_from_file
    # scenario 3 (yet to be implemented)


def final_analysis(argument, input_sizes, command):
    all_the_times = []
    for iteration in range(0, 10):
        all_the_times.append(execute_commands(argument, input_sizes, command))

    axes = []
    avg = 0
    # TODO get better names for these variables as its confusing asf.

    # The value return from execute_commands is a list of lists, where each element is a list containing the 8 times
    # of each input_size. If there are more than 1 elements in this list, then that menas "all" was requested, and
    # there are 3 lists (containing 8 elements each) containing the times for each data structure's algorithm (A, D, etc).

    # need to handle the case where only 1 structure is requested, and other case where all 3 are requested ("all").

    for times in all_the_times:
        for agent_time in times:

            axes.append(AxisPair(input_sizes, agent_time))

    plot_graph(axes, input_sizes[0], input_sizes[-1])


def get_word_freq_list(n):
    words_frequencies_from_file = []
    data_file = open("input_" + n, 'r')
    for line in data_file:
        values = line.split()
        word = values[0]
        frequency = int(values[1])
        word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
        words_frequencies_from_file.append(word_frequency)
    data_file.close()
    return words_frequencies_from_file


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
