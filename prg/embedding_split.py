import numpy as np
import math
import os
import tqdm
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.signal import argrelextrema
from typing import List
from prg.plot import plot_similarities, plot_relative_minimas
from prg.utils import save_paragraphs
from prg.plot import plot_size_repartition


def encode_sentences(sentences: List[str], model_name: str = "all-mpnet-base-v2", batch_size: int = 32) -> List[List[float]]:
    """
    Encode a list of sentences using SentenceTransformer model.

    Parameters:
    - sentences (List[str]): List of sentences to be encoded.
    - model_name (str): Name or path of the SentenceTransformer model. Default is 'all-mpnet-base-v2'.

    Returns:
    - List[List[float]]: List of sentence embeddings.
    """
    print(f"Loading model {model_name}")

    # Specify device (use GPU if available, otherwise use CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Load the SentenceTransformer model with the specified device
    model = SentenceTransformer(model_name, device=device)

    print("Getting embedding")

    # Encode sentences
    embeddings = np.empty((0, model.get_sentence_embedding_dimension()))

    for batch in tqdm.tqdm(range(0, len(sentences), batch_size)):
        batch_sentences = sentences[batch:batch + batch_size]
        batch_embeddings = model.encode(batch_sentences, batch_size=batch_size)
        embeddings = np.concatenate((embeddings, np.array(batch_embeddings)))

    print(f"Embedding shape {embeddings.shape} ")

    return embeddings


def get_cosine_similarity(
    embeddings: List[List[float]], output_path: str, save: bool = False, display: bool = False
):
    """
    Plot cosine similarities matrix using seaborn's heatmap.

    Parameters:
    - embeddings (List[List[float]]): List of sentence embeddings.
    - save (bool): Whether to save the plot as an image. Default is False.
    """
    # Create similarities matrix
    similarities = cosine_similarity(embeddings)

    # Check if the shape of embeddings is less than 100
    if len(embeddings) < 100 and save:
        plot_similarities(similarities, output_path, save, display)
    elif len(embeddings) > 100 and save:
        print(
            "The shape of embeddings is greater than or equal to 100. Plotting is skipped."
        )

    return similarities


def rev_sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(0.5 * x))


def activate_similarities(similarities: np.array, p_size: int = 10) -> np.array:
    """ Function returns list of weighted sums of activated sentence similarities
        Args:
            similarities (numpy array): it should square matrix where each sentence corresponds to another with cosine sim
            p_size (int): number of sentences are used to calculate weighted sum
        Returns:
            list: list of weighted sums
        """
    # To create weights for sigmoid function we first have to create space.
    # P_size will determine number of sentences used and the size of weights vector.
    x = np.linspace(-10, 10, p_size)
    # Then we need to apply activation function to the created space
    y = np.vectorize(rev_sigmoid)
    # Because we only apply activation to p_size number of sentences we have to add
    # zeros to neglect the effect of every additional sentence and to match the length ofvector we will multiply
    activation_weights = np.pad(y(x), (0, similarities.shape[0] - p_size))
    # 1. Take each diagonal to the right of the main diagonal
    diagonals = [
        similarities.diagonal(each) for each in range(0, similarities.shape[0])
    ]
    # 2. Pad each diagonal by zeros at the end.
    # Because each diagonal is different length we should pad it with zeros at the end
    diagonals = [
        np.pad(each, (0, similarities.shape[0] - len(each))) for each in diagonals
    ]
    # 3. Stack those diagonals into new matrix
    diagonals = np.stack(diagonals)
    # 4. Apply activation weights to each row. Multiply similarities with our activation.
    diagonals = diagonals * activation_weights.reshape(-1, 1)
    # 5. Calculate the weighted sum of activated similarities
    activated_similarities = np.sum(diagonals, axis=0)
    return activated_similarities


def get_minimas(
    activated_similarities: np.array, order: int, output_path: str, save: bool = False, display: bool = False
):
    # order parameter controls how frequent should be splits. I would not reccomend changing this parameter.
    minimas = argrelextrema(activated_similarities, np.less, order=order)

    if save:
        plot_relative_minimas(minimas, activated_similarities, output_path, save, display)

    return minimas


def create_paragraphs_at_minimas(sentences: List[str], minimas: List[int]) -> List[str]:
    """
    Create paragraphs at specified minimas in the list of sentences.

    Parameters:
    - sentences (List[str]): List of sentences.
    - minimas (List[int]): List of indices where paragraphs should be created.

    Returns:
    - List[str]: List of paragraphs.
    """
    # Get the order number of the sentences which are in splitting points
    split_points = [each for each in minimas[0]]

    # Initialize variables
    line = ""
    paragraphs = []

    for num, each in enumerate(sentences):
        # Check if sentence is a minima (splitting point)
        if num in split_points:
            # If it is, add a dot to the end of the sentence and start a new paragraph
            line += f"{each}"
            paragraphs.append(line)
            line = ""
        else:
            # If it is a normal sentence, just add a dot to the end and keep adding sentences to the line
            line += f"{each}. "

    return paragraphs


def paragraphs_by_embedding(sentences: List[str], output_path: str, file_name: str, save: bool, display: bool, batch_size: int) -> List[str]:
    """
    Take a list of sentences and split them into paragraphes
    return the list of paragraphes
    """
    embeddings = encode_sentences(sentences, batch_size=batch_size)

    similarities = get_cosine_similarity(
        embeddings,
        os.path.join(output_path, "Cosine_similarities_matrix.png"),
        save,
        display
    )

    activated_similarities = activate_similarities(similarities, p_size=2)

    # Increase Order to reduce number of paragraphe
    minimas = get_minimas(
        activated_similarities,
        1,
        os.path.join(output_path, "Relative_minimas.png"),
        save,
        display,
    )

    if len(minimas[0]):
        paragraphs = create_paragraphs_at_minimas(sentences, minimas)
    else:
        paragraphs = ''.join(sentences)

    if display and output_path:
        plot_size_repartition(
            paragraphs,
            os.path.join(output_path, "paragraphes_distribution.png"),
            save, display, True
        )

    if save :
        save_paragraphs(paragraphs, os.path.join(output_path, f"paragraphe_{file_name}.txt"))

    return paragraphs