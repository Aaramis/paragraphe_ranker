import os
from prg.config import parse_args, check_arguments
from prg.file_reader import extract_text_from_document
from prg.utils import (
    sentences_homogeneisation,
    create_sentences,
)
from prg.embedding_split import paragraphs_by_embedding


def main():

    # Initialization
    args = parse_args()
    check_arguments(args)

    # Text extraction
    text = extract_text_from_document(os.path.join(args.file_path, args.file_name))

    sentences = create_sentences(text)
    # plot_size_repartition(sentences, os.path.join(args.output_path, "rep_pre_traitement.png"), False)

    sentences = sentences_homogeneisation(sentences)
    # plot_size_repartition(sentences, os.path.join(args.output_path, "sentences_traited.png"), args.save_plots)

    if args.mode == "embedding":
        paragraphs = paragraphs_by_embedding(sentences, args.output_path, args.file_name, args.save_plots)


if __name__ == "__main__":
    main()
