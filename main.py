import os
from src.config import parse_args, check_arguments
from src.file_reader import extract_text_from_document
from src.utils import (
    sentences_homogeneisation,
    create_sentences,
    save_paragraphs,
)
from src.plot import plot_size_repartition
from src.embedding_split import (
    encode_sentences,
    get_cosine_similarity,
    activate_similarities,
    get_minimas,
    create_paragraphs_at_minimas,
)


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

    embeddings = encode_sentences(sentences)

    similarities = get_cosine_similarity(
        embeddings,
        os.path.join(args.output_path, "Cosine_similarities_matrix.png"),
        args.save_plots
        )

    activated_similarities = activate_similarities(similarities, p_size=2)

    # Increase Order to reduce number of paragraphe
    minimas = get_minimas(activated_similarities, 1, os.path.join(args.output_path, "Relative_minimas.png"), args.save_plots)

    paragraphs = create_paragraphs_at_minimas(sentences, minimas)

    plot_size_repartition(paragraphs, os.path.join(args.output_path, "paragraphes_distribution.png"), True)

    save_paragraphs(paragraphs, os.path.join(args.output_path, f"paragraphe_{ args.file_name}.txt"))


if __name__ == "__main__":
    main()
