# written by Heike von Waaden - Heike.vonWaaden@yahoo.de, 10-08-2024

import argparse
import json
import matplotlib.pyplot as plt
import sys
from pathlib import Path

from openfast_toolbox.io import FASTOutputFile


def plot_dataframe_columns(df_outb, data, output_path, plot_title):
    # Create subplots for each set of variables
    fig, axes = plt.subplots(nrows=len(data), ncols=1, sharex=True, figsize=(12, 2 * len(data)))

    # Plot each set of variables in a separate subplot
    for i, entry in enumerate(data):
        variables = entry["variables"]
        colors = entry["colors"]
        linestyles = entry["linestyles"]

        # Plot each variable in the set
        for j, variable in enumerate(variables):
            ax = axes[i]
            ax.plot(df_outb["Time_[s]"], df_outb[variable], color=colors[j], linestyle=linestyles[j], label=variable)

        # Add a light grid with higher discretization on the x-axis
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=20))
        ax.grid(True, linestyle="dotted", alpha=0.6)


        # Set ylabel for the subplot
        ax.set_ylabel("\n".join(variables))
        labelx = -0.075  # axes coords
        ax.yaxis.set_label_coords(labelx, 0.5)

    # Set x-axis label and title for the entire plot
    plt.xlabel("Time_[s]")

    # Add a title on top of the entire plot
    plt.suptitle(plot_title, y=0.95, fontsize=16)

    # Save the plot to the specified output path
    plt.savefig(output_path, bbox_inches="tight")

def get_arguments():
    parser = argparse.ArgumentParser(description="Create png form binary OpenFast time series (*.outb) ...")

    parser.add_argument(
        "-l",
        help="Variables and colors list - see example",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-i",
        help="Get path for *.outb file",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    return args

# Example usage
if __name__ == "__main__":
    # read arguments
    args = get_arguments()

    if args.l is not None:
        if Path(args.l).is_file():
            # read line of path_list
            path_cc = args.l

    if args.i is not None:
        if Path(args.i).is_file():
            # read line of path_list
            input_path = args.i


    # Read JSON data from the file
    with open(path_cc, 'r') as file:
        json_data = file.read()

    # Parse the JSON data
    data = json.loads(json_data)


    # Read the dataframe from the CSV file
    df_outb = FASTOutputFile(input_path).toDataFrame()

    # Set the output path for the PNG file
    output_path = input_path + '.png'

    # Add a title on top of the entire plot
    title = output_path.split('\\')
    plot_title = title[-1].replace('.png', '')

    # Call the function to plot and save the figure
    plot_dataframe_columns(df_outb, data, output_path, plot_title)


    # plt.show()
    print('\nPNG is successfully generated and stored here:\n' + output_path)
