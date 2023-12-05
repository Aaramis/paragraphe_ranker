import matplotlib.pyplot as plt
import seaborn as sns
from typing import List


def plot_size_repartition(my_list: List[str], output_path: str, save: bool, word:bool = False) -> None:

    # Create a new figure for each call
    fig, ax = plt.subplots()

    if word :
        plt.plot(sorted([len(i.split()) for i in my_list]))
    else :
        plt.plot(sorted([len(i) for i in my_list]))

    if save:
        plt.savefig(output_path)


def plot_similarities(similarities: List[str], output_path: str, save: bool) -> None:

    # Plot the result
    sns.heatmap(similarities, annot=True).set_title("Cosine similarities matrix")

    # Save the plot if save is True
    if save:
        plt.savefig(output_path)


def plot_relative_minimas(
    minimas, activated_similarities, output_path: str, save: bool
) -> None:

    # Create a new figure for each call
    fig, ax = plt.subplots()

    # Plot the flow of our text with activated similarities
    sns.lineplot(
        y=activated_similarities, x=range(len(activated_similarities)), ax=ax
    ).set_title("Relative minimas")
    # Plot vertical lines in order to see where we created the split
    plt.vlines(
        x=minimas,
        ymin=min(activated_similarities),
        ymax=max(activated_similarities),
        colors="purple",
        ls="--",
        lw=1,
        label="vline_multiple - full height",
    )

    # Save the plot if save is True
    if save:
        plt.savefig(output_path)
