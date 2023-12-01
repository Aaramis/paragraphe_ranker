import numpy as np
from typing import List


def create_sentences(text: str) -> List[str]:
    sentences = text.split(". ")
    # Add a dot at the end of each element
    sentences_with_dot = [sentence + ". " for sentence in sentences]
    return sentences_with_dot


def remove_short_sentences(sentences: List[str], size: int = 25) -> List[str]:
    return [element for element in sentences if len(element) > size]


def sentences_homogeneisation(sentences: List[str]) -> List[str]:
    # Get the length of each sentence
    sentence_length = [len(each) for each in sentences]

    # Determine deciles
    deciles = [np.percentile(sentence_length, i) for i in range(10, 91, 10)]

    # Determin deciles to remove
    long = deciles[8]
    short = deciles[1]

    # Process sentences
    text = ""
    for each in sentences:
        if len(each) > long:
            each = each.replace(",", ". ")
            text += f"{each}"
        else:
            text += f"{each}"
    sentences = create_sentences(text)

    # Now let's concatenate short ones
    text = ""
    for each in sentences:
        if len(each) < short:
            each = each.replace(".", " ")
            text += f"{each}"
        else:
            text += f"{each}"

    # sentences = create_sentences(text)
    return create_sentences(text)


def save_paragraphs(paragraphs: List[str], output_path: str) -> None:
    """
    Save paragraphs to a text file.

    Parameters:
    - paragraphs (List[str]): List of paragraphs to be saved.
    - output_path (str): Path to the output text file.
    """
    print(f"Number of paragraphs: {len(paragraphs)}")

    with open(output_path, "w") as fout:
        for sentence in paragraphs:
            fout.write(sentence + "\n")
