from typing import List

from axis_pair import AxisPair
import matplotlib.pyplot as plt
import numpy as np


def plot_line_graph(axes: List[AxisPair], x_axis_min: str, x_axis_max: str, algorithm: str,
                    num_of_algorithm_iterations: int):
    if len(axes) <= 0:
        return

    for idx, axes_pair in enumerate(axes):
        title = "List"

        if idx == 1:
            title = "Hashtable"
        elif idx == 2:
            title = "TST"

        print(axes_pair.x_axis, axes_pair.y_axis)
        plt.plot(axes_pair.x_axis, axes_pair.y_axis, label=title)

    if algorithm == 's':
        graph_title = 'Search Benchmark'
    elif algorithm == 'a':
        graph_title = 'Add Benchmark'
    elif algorithm == 'd':
        graph_title = 'Delete Benchmark'
    else:
        graph_title = 'Autocomplete Benchmark'

    plt.xlabel('Number of Elements before Operation')
    plt.xlim(x_axis_min, x_axis_max)
    plt.ylabel('Log of Time per ' + str(num_of_algorithm_iterations) + ' Operations (ns)')
    plt.title(graph_title)
    plt.legend(loc="upper left")
    plt.show()


def display_numerical_data(data, decimal_accuracy, algorithm_shorthand_to_longhand, valid_approaches,
                           valid_algorithms_shorthand, approach_titles):
    for idx, approach in enumerate(valid_approaches):
        print("{:^97s}".format("### " + approach_titles[idx] + " Results ###"))
        for algorithm in valid_algorithms_shorthand:
            if len(data[approach][algorithm]) <= 0:
                continue

            print("{:^97s}".format(algorithm_shorthand_to_longhand[algorithm] + " Algorithm"))
            print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format('50', '500', '1k', '2k', '5k', '10k',
                                                                                   '50k',
                                                                                   '100k'))
            nums_to_display = []
            for x in data[approach][algorithm]:
                nums_to_display.append(round(x, decimal_accuracy))

            print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(*nums_to_display))
            print()

        print('\n')


def plot_singular_bar_chart(titles, data):
    plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(titles, data, color='maroon',
            width=0.4)

    plt.title("Overall Algorithm Efficiency")
    plt.xlabel('Approach', fontweight='bold', fontsize=15)
    plt.ylabel('Overall Efficiency Score', fontweight='bold', fontsize=15)
    plt.show()


def plot_multi_bar_chart(data: list, x_titles: list):
    # set width of bar
    bar_width = 0.25
    plt.subplots(figsize=(12, 8))

    # Set position of bar on X axis
    br1 = np.arange(len(data[0]))
    br2 = [x + bar_width for x in br1]
    br3 = [x + bar_width for x in br2]

    # Make the plot
    plt.bar(br1, data[0], color='r', width=bar_width,
            edgecolor='grey', label='List')
    plt.bar(br2, data[1], color='y', width=bar_width,
            edgecolor='grey', label='Hashtable')
    plt.bar(br3, data[2], color='g', width=bar_width,
            edgecolor='grey', label='TST')

    # Adding Xticks
    plt.xlabel('Algorithm', fontweight='bold', fontsize=15)
    plt.ylabel('Time', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(data[0]))],
               x_titles)

    plt.legend()
    plt.show()
