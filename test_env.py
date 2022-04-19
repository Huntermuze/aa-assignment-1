import sys
import timeit
import matplotlib.pyplot as plt
from dictionary.node import Node
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary

def usage():
    """
    Print help/usage message.
    """
    print('python3 test_env.py', '<approach>')
    print('<approach> = <list | hashtable | tst>')
    sys.exit(1)

def execute_command(agent, input_sizes, command):
    word_freq_to_add = get_eight_objects(command)
    times = []
    i = 0
    
    for n in input_sizes:
        agent.build_dictionary(get_word_freq_list(n))
        if command == 'S':
            times.append(timeit.timeit(lambda: agent.search(word_freq_to_add[i]), number=1))
        elif command == 'A':
            times.append(timeit.timeit(lambda: agent.add_word_frequency(word_freq_to_add[i]), number=1))
        elif command == 'D':
            times.append(timeit.timeit(lambda: agent.delete_word(word_freq_to_add[i]), number=1))
        elif command == 'AC':
            times.append(timeit.timeit(lambda: agent.autocomplete(word_freq_to_add[i]), number=1))
        print("Time " + str(i + 1) + ": " + str(times[i]))
        i += 1
    plt.plot(input_sizes, times)
    plt.xlabel('Number of Elements')
    plt.ylabel('Time for Operation')
    plt.title('Benchmarking')
    plt.show()
    return

def get_eight_objects(command):
    words_frequencies_from_file = []
    # scenario 1
    if command == 'A':
        data_file = open("eight_inputs_add", 'r')
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

if __name__ == '__main__':
    input_sizes_grow = ['50', '500', '1k', '2k', '5k', '10k', '50k', '100k']
    input_sizes_shrink = ['100k', '50k', '10k', '5k', '2k', '1k', '500', '50']
    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 2:
        print('Incorrect number of arguments.')
        usage()

    # initialise search agent
    agent: BaseDictionary = None
    if args[1] == 'list':
        agent = ListDictionary()
    elif args[1] == 'hashtable':
        agent = HashTableDictionary()
    elif args[1] == 'tst':
        agent = TernarySearchTreeDictionary()
    else:
        print('Incorrect argument value.')
        usage()

    # search
    command = input("Please enter a command (S, A, D, AC): ")
    if command == 'S' or command == 'A' or command == 'D' or command == 'AC':
        execute_command(agent, input_sizes_grow, command)
    else:
        print('Unknown command.')