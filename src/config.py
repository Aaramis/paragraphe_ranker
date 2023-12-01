import argparse
import os


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Text To Paragraphe Configuration")

    # Command line arguments for directory and files
    main_args = parser.add_argument_group("Directory arguments")
    main_args.add_argument(
        "--file_path",
        type=str,
        default=os.path.abspath("./books/pdf"),
        help="Path to the data directory",
    )
    main_args.add_argument(
        "--file_name",
        type=str,
        default="medium_sentence_to_paragraph.pdf",
        help="file name",
    )
    main_args.add_argument(
        "--queries_path",
        "-o",
        type=str,
        default=os.path.abspath("./queries"),
        help="Path to the queries directory",
    )
    main_args.add_argument(
        "--queries_name",
        type=str,
        default="qa_pairs_myxomycetes.tsv",
        help="Querie file name",
    )
    main_args.add_argument(
        "--output_path",
        type=str,
        default="./output",
        help="Querie file name",
    )
    main_args.add_argument(
        "--save_plots",
        action="store_true",
        help="Flag to trigger plotting."
    )
    main_args.add_argument(
        "--mode",
        type=str,
        help="Choose the methode you need [embedding | simple]",
        default="embedding",
    )
    return parser.parse_args()


def check_directory(path: str) -> None:
    """Check if the directory exists or create it."""
    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            print(f"'{path}' is not a valid. EXIT")
            exit()


def check_arguments(options: argparse.Namespace) -> None:
    check_directory(options.output_path)
