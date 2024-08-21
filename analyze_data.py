import json
import os
import numpy as np


def verify_answers(path):
    histogram = []
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
    answers_to_verify = data
    for entry in answers_to_verify:
        succsees_rate = entry['succsees_rate']
        histogram.append(succsees_rate)

    print(histogram)
    return histogram


path = "VERIFIED_OUTPUT/"
dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")

# print the list
print(dir_list)
for path in dir_list:
    output_file_path = "VERIFIED_OUTPUT/" + path

    histogram = verify_answers(output_file_path)

    import matplotlib.pyplot as plt

    bins = np.arange(0, 1.05, 0.05)

    # Calculate the histogram
    counts, bin_edges = np.histogram(histogram, bins=bins)

    # Normalize by the size of the data
    counts_normalized = counts / len(histogram)

    # Plot the normalized histogram
    plt.bar(bin_edges[:-1], counts_normalized, width=0.05, edgecolor='black', align='edge')

    # Set y-ticks at specific intervals
    plt.yticks(np.arange(0, 1.1, 0.1))

    # Convert y-axis to percentage
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

    # Add horizontal grid lines at the y-ticks
    plt.grid(axis='y', linestyle='--')

    # Add colored backgrounds for specified x-value ranges
    plt.axvspan(0, 0.1, color='red', alpha=0.3)
    plt.axvspan(0.1, 0.25, color='orange', alpha=0.3)
    plt.axvspan(0.25, 0.75, color='yellow', alpha=0.3)
    plt.axvspan(0.75, 0.9, color='chartreuse', alpha=0.3)
    plt.axvspan(0.9, 1.0, color='green', alpha=0.3)

    # Add title and labels
    plt.title(path[:-5])
    plt.xlabel('Success rate')
    plt.ylabel('probability')

    # Set y-axis range from 0 to 1
    plt.ylim(0, 1)

    # Save the plot as a PNG file
    plt.savefig('PLOT/' + path[:-5] + '.png', format='png')

    # Show the plot
    plt.show()
