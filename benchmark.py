import math
import sys
import timeit
import random
from display import *
from typing import List
from axis_pair import AxisPair
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary

n_mapped_to_int = {'50': 50, '500': 500, '1k': 1000, '2k': 2000, '5k': 5000, '10k': 10000, '50k': 50000, '100k': 100000}
input_sizes = ['50', '500', '1k', '2k', '5k', '10k', '50k', '100k']
reversed_input_sizes = ['100k', '50k', '10k', '5k', '2k', '1k', '500', '50']
valid_output_types = ['graphic', 'numeric']
valid_approaches = ['list', 'hashtable', 'tst']
valid_algorithms_shorthand = ['s', 'a', 'd', 'ac']
valid_representation_types = ['1', '2']
approach_titles = ['List', 'Hashtable', 'Ternary Search Tree']
algorithm_titles = ['Search', 'Add', 'Delete', 'Auto-Complete']
algorithm_shorthand_to_longhand = {'s': 'Search', 'a': 'Add', 'd': 'Delete', 'ac': 'AutoComplete'}
cached_input_from_file = {}

s_to_ns_scalar = 1000 * 1000 * 1000


def display_usage():
    print('python3 benchmark.py', '<approach>')
    print('where <approach> = <list | hashtable | tst | all>')
    sys.exit(1)


def main():
    # Fetch the algorithm line arguments
    args = sys.argv

    if len(args) != 2:
        print('Incorrect number of arguments.')
        display_usage()

    algorithm = input("Please enter an algorithm to run (s, a, d, ac, all): ").lower()
    output_type = input("Please enter the type of output you wish to receive (graphic, numeric): ").lower()
    approach = args[1]
    representation_type = None
    if output_type == 'graphic' and approach == 'all' and algorithm == 'all':
        representation_type = input("Would you prefer (enter 1 or 2):"
                                    "\n1. Display all approaches and their algorithm's runtime side-by-side (12 bars)."
                                    "\n2. Display a graph representing each approaches total score (calculated based on "
                                    "the average of all algorithm's performance for each approach).\n")

    if approach not in valid_approaches + ['all']:
        print('Unknown approach type.')
        sys.exit(1)

    if algorithm not in valid_algorithms_shorthand + ['all']:
        print('Unknown algorithm.')
        sys.exit(1)

    if output_type not in valid_output_types:
        print('Unknown output type.')
        sys.exit(1)

    if representation_type is not None and representation_type not in valid_representation_types:
        print('Unknown representation type.')
        sys.exit(1)

    final_analysis(approach, algorithm, output_type, representation_type)


def final_analysis(approach_arg: str, algorithm_arg: str, output_type_arg: str, representation_type):
    adds_to_choose_from = get_input_from_file("input/input_adds", True)
    num_of_algorithm_iterations = 50
    upper_bound = 10

    # Contains each approach, and each approach's algorithm times. Approach -> Algorithm -> 8 Times.
    all_approaches_and_algorithms_times = {
        'list': {'s': [], 'a': [], 'd': [], 'ac': []},
        'hashtable': {'s': [], 'a': [], 'd': [], 'ac': []},
        'tst': {'s': [], 'a': [], 'd': [], 'ac': []}
    }

    for iteration in range(0, upper_bound):
        print("\n\n #### >>> RUN " + str(iteration + 1) + " <<< ####\n\n")
        approach_and_algorithm_times = execute_and_time_algorithms(approach_arg, algorithm_arg,
                                                                   num_of_algorithm_iterations, adds_to_choose_from,
                                                                   output_type_arg == 'graphic')

        for approach in valid_approaches:
            for algorithm in valid_algorithms_shorthand:
                input_size_times = approach_and_algorithm_times[approach][algorithm]

                if len(input_size_times) == 8 and upper_bound <= 1:
                    all_approaches_and_algorithms_times[approach][algorithm] = input_size_times
                if len(input_size_times) == 8 and upper_bound > 1:
                    all_approaches_and_algorithms_times[approach][algorithm].append(input_size_times)

    for approach in valid_approaches:
        for algorithm in valid_algorithms_shorthand:
            if len(all_approaches_and_algorithms_times[approach][algorithm]) == 0:
                continue

            arr = np.array(all_approaches_and_algorithms_times[approach][algorithm])
            all_approaches_and_algorithms_times[approach][algorithm] = np.average(arr, axis=0)

    if output_type_arg == 'graphic':
        axes = []

        if algorithm_arg == 'd':
            inp = reversed_input_sizes
        else:
            inp = input_sizes

        if approach_arg == 'all' and algorithm_arg == 'all' and representation_type == '1':
            results = []

            for idx, approach in enumerate(valid_approaches):
                results.append([])
                for algorithm in valid_algorithms_shorthand:
                    results[idx].append(np.average(all_approaches_and_algorithms_times[approach][algorithm]))

            plot_multi_bar_chart(results, algorithm_titles)
            return
        elif approach_arg == 'all' and algorithm_arg == 'all' and representation_type == '2':
            results = []

            for idx, approach in enumerate(valid_approaches):
                results.append([])
                for algorithm in valid_algorithms_shorthand:
                    results[idx].append(np.average(all_approaches_and_algorithms_times[approach][algorithm]))

                results[idx] = np.average(results[idx])

            plot_singular_bar_chart(approach_titles, results)
            return
        elif approach_arg != 'all' and algorithm_arg == 'all':
            results = []

            for algorithm in valid_algorithms_shorthand:
                arr = np.array(all_approaches_and_algorithms_times[approach_arg][algorithm])
                results.append(np.average(arr, axis=0))

            plot_singular_bar_chart(algorithm_titles, results)
            return
        elif approach_arg == 'all' and algorithm_arg != 'all':
            for approach in valid_approaches:
                arr = np.array(all_approaches_and_algorithms_times[approach][algorithm_arg])
                axes.append(AxisPair(inp, arr))

        elif approach_arg != 'all' and algorithm_arg != 'all':
            arr = np.array(all_approaches_and_algorithms_times[approach_arg][algorithm_arg])
            axes.append(AxisPair(inp, arr))

        plot_line_graph(axes, inp[0], inp[-1], algorithm_arg, num_of_algorithm_iterations)
    else:
        display_numerical_data(all_approaches_and_algorithms_times, 3, algorithm_shorthand_to_longhand,
                               valid_approaches, valid_algorithms_shorthand, approach_titles)


def execute_and_time_algorithms(approach_arg: str, algorithm_arg: str, num_of_algorithm_iterations: int,
                                adds_to_choose_from: List[WordFrequency], log_time: bool) -> dict:
    prebuilt_dictionaries = get_prebuilt_dictionaries(approach_arg, algorithm_arg)
    approach_and_algorithm_times = prebuilt_dictionaries

    for approach, algorithms in prebuilt_dictionaries.items():
        print("\n#### " + approach.upper() + " APPROACH ####")
        for algorithm, inp_sizes in algorithms.items():
            print("\nALGORITHM: " + algorithm_shorthand_to_longhand[algorithm])
            for index, dictionary in enumerate(inp_sizes):
                dictionary_to_test = prebuilt_dictionaries[approach][algorithm][index]
                # In nanoseconds.
                sum_of_running_times = 0

                word_freqs_to_process = get_random_algorithm_input(algorithm,
                                                                   get_input_from_file(
                                                                       "input/input_" + input_sizes[index], True),
                                                                   input_sizes[index],
                                                                   num_of_algorithm_iterations,
                                                                   adds_to_choose_from)

                if algorithm == 's':
                    method_to_time = dictionary_to_test.search
                elif algorithm == 'a':
                    method_to_time = dictionary_to_test.add_word_frequency
                elif algorithm == 'd':
                    method_to_time = dictionary_to_test.delete_word
                else:
                    method_to_time = dictionary_to_test.autocomplete

                for word_freq in word_freqs_to_process:
                    sum_of_running_times += timeit.timeit(lambda: method_to_time(word_freq), number=1) * s_to_ns_scalar

                average_running_time = sum_of_running_times / num_of_algorithm_iterations

                if log_time:
                    time = math.log(average_running_time, 10)
                else:
                    time = average_running_time

                # Replace the dictionary with the logged average running time in the nested dictionary to prepare it
                # for garbage collection and to prevent creation of an entirely new data structure and the copy ops.
                approach_and_algorithm_times[approach][algorithm][index] = time

                unit = "log(ns)" if log_time else "ns"

                if algorithm == 'd':
                    inp = reversed_input_sizes
                else:
                    inp = input_sizes

                print("Input Size [" + inp[index] + "] Time {" + unit + "} > " + str(time))

    return approach_and_algorithm_times


def get_prebuilt_dictionaries(approach_arg: str, algorithm_arg: str):
    prebuilt_dicts = {
        'list': {'s': [], 'a': [], 'd': [], 'ac': []},
        'hashtable': {'s': [], 'a': [], 'd': [], 'ac': []},
        'tst': {'s': [], 'a': [], 'd': [], 'ac': []}
    }

    if approach_arg == 'all' and algorithm_arg == 'all':
        for approach in valid_approaches:
            for algorithm in valid_algorithms_shorthand:
                for size in reversed_input_sizes if algorithm == 'd' else input_sizes:
                    prebuilt_dicts[approach][algorithm].append(create_and_build_dict(approach, size))
    elif approach_arg == 'all' and algorithm_arg != 'all':
        for approach in valid_approaches:
            for size in input_sizes:
                prebuilt_dicts[approach][algorithm_arg].append(create_and_build_dict(approach, size))
    elif approach_arg != 'all' and algorithm_arg == 'all':
        for algorithm in valid_algorithms_shorthand:
            for size in reversed_input_sizes if algorithm == 'd' else input_sizes:
                prebuilt_dicts[approach_arg][algorithm].append(create_and_build_dict(approach_arg, size))
    else:
        for size in reversed_input_sizes if algorithm_arg == 'd' else input_sizes:
            prebuilt_dicts[approach_arg][algorithm_arg].append(create_and_build_dict(approach_arg, size))

    return prebuilt_dicts


def create_and_build_dict(approach: str, input_size: str) -> BaseDictionary:
    if approach == 'list':
        dict_to_add = ListDictionary()
    elif approach == 'hashtable':
        dict_to_add = HashTableDictionary()
    else:
        dict_to_add = TernarySearchTreeDictionary()

    dict_to_add.build_dictionary(get_input_from_file("input/input_" + input_size, True))

    return dict_to_add


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
                # If there is only a word and no frequency (i.e., delete, search or autocomplete algorithms).
                else:
                    input_from_file.append(word)

        # Add to the cached input list to speedup the benchmarking.
        cached_input_from_file[input_size] = input_from_file

    return cached_input_from_file[input_size]


def get_random_algorithm_input(algorithm: str, word_frequencies_from_file: List[WordFrequency], n: str,
                               num_of_algorithm_iterations: int, adds_to_choose_from: List[WordFrequency]) -> list:
    algorithm_input = []
    max_num = n_mapped_to_int[n]

    # Scenario 1 grow
    if algorithm == 'a':
        max_adds = len(adds_to_choose_from)
        for i in range(0, num_of_algorithm_iterations):
            algorithm_input.append(adds_to_choose_from[random.randint(0, max_adds - 1)])
    # Scenario 2 shrink + Scenario 3 search
    elif algorithm == 'd' or algorithm == 's':
        for i in range(0, num_of_algorithm_iterations):
            algorithm_input.append(word_frequencies_from_file[random.randint(0, max_num - 1)].word)
    # Scenario 3 autocomplete
    else:
        for i in range(0, num_of_algorithm_iterations):
            picked_word = word_frequencies_from_file[random.randint(0, max_num - 1)].word
            if len(picked_word) <= 4:
                cur_ac = len(picked_word)
            else:
                cur_ac = 5
            algorithm_input.append(picked_word[0:random.randint(1, cur_ac)])

    return algorithm_input


if __name__ == '__main__':
    main()
