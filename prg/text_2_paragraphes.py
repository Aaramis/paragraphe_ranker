import os
from prg.config import check_directory
from prg.file_reader import extract_text_from_document
from prg.utils import (
    sentences_homogeneisation,
    create_sentences,
)
from prg.embedding_split import paragraphs_by_embedding
from prg.simple import simple_paragraphs


def create_paragraphes(text: str, mode: str, display_plots: bool, batch_size: int = 32, nb_sentences: int = 500):
    sentences = create_sentences(text)
    # plot_size_repartition(sentences, os.path.join(output_path, "rep_pre_traitement.png"), False)

    sentences = sentences_homogeneisation(sentences)
    # plot_size_repartition(sentences, os.path.join(output_path, "sentences_traited.png"), save_plots)

    if mode == "embedding":
        paragraphs = paragraphs_by_embedding(sentences, "./", None, save = False,
                                             display = display_plots,
                                             batch_size=batch_size,
                                             nb_sentences=nb_sentences)
    
    elif mode == "simple":
        paragraphs = simple_paragraphs(sentences,  "./", None, save = False, display = display_plots, max_word_count=100)
    
    return paragraphs

# def create_paragraphes(file_path: str, file_name: str, output_path: str, mode: str, save_plots: bool, display_plots: bool):
#     """
#     Create paragraphs from a text document using either simple or embedding-based processing.

#     Parameters:
#     - file_path (str): The path to the directory containing the input text document.
#     - file_name (str): The name of the input text document.
#     - output_path (str): The path to the directory where output files and plots will be saved.
#     - mode (str): The processing mode, either 'embedding' for advanced processing or 'simple' for basic processing.
#     - save_plots (bool): Whether to save plots generated during processing.

#     Returns:
#     - List[str]: A list of paragraphs created from the input text document.
#     """
    
#     check_directory(output_path)

#     # Text extraction
#     text = extract_text_from_document(os.path.join(file_path, file_name))

#     sentences = create_sentences(text)
#     # plot_size_repartition(sentences, os.path.join(output_path, "rep_pre_traitement.png"), False)

#     sentences = sentences_homogeneisation(sentences)
#     # plot_size_repartition(sentences, os.path.join(output_path, "sentences_traited.png"), save_plots)

#     if mode == "embedding":
#         paragraphs = paragraphs_by_embedding(sentences, output_path, file_name, save_plots)
    
#     elif mode == "simple":
#         paragraphs = simple_paragraphs(sentences, output_path, file_name, save_plots, 100)

#     return paragraphs

