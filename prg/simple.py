import re
import os
import unicodedata
from prg.utils import save_paragraphs
from prg.plot import plot_size_repartition

def simple_paragraphs(sentences, output_path, file_name, save_plots, max_word_count=100):
    """
    Create paragraphs from a list of sentences with a maximum word count constraint.

    Parameters:
    - sentences (list): List of sentences to be grouped into paragraphs.
    - output_path (str): The path to the directory where output files and plots will be saved.
    - file_name (str): The name of the input file, used for generating unique output filenames.
    - save_plots (bool): Whether to save plots generated during processing.
    - max_word_count (int): Maximum word count for each paragraph. Default is 100.

    Returns:
    - list: List of paragraphs created from the input sentences.
    """
    paragraphs = []
    current_sentence = ""

    for sentence in sentences:
        # Preprocess sentence
        sentence = re.sub(' +', ' ', sentence.replace("\n", "").replace("\t", ""))

        # Check if adding the sentence exceeds the word count limit
        if len(current_sentence.split(" ")) + len(sentence.split(" ")) < max_word_count:
            current_sentence += sentence + ". "
        else:
            # Append the current sentence as a paragraph
            paragraphs.append(unicodedata.normalize("NFKD", current_sentence))
            # Reset current sentence with the new sentence
            current_sentence = sentence + ". "

    # Append any remaining sentence as the last paragraph
    if current_sentence:
        paragraphs.append(unicodedata.normalize("NFKD", current_sentence))


    plot_size_repartition(
        paragraphs, os.path.join(output_path, "paragraphes_distribution.png"), save_plots
    )

    save_paragraphs(
        paragraphs, os.path.join(output_path, f"paragraphe_{file_name}.txt")
    )

    return paragraphs
