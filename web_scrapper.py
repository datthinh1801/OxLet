from subprocess import check_output
from bs4 import BeautifulSoup
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--words",
        nargs="?",
        help="a list of words/phrases separated by commas (e.g. sustainable, take a toll)",
        type=str,
        dest="words",
    )
    parser.add_argument(
        "-f",
        "--file",
        nargs="?",
        help="the name of the file to read from (e.g. newwords.txt)",
        type=str,
        dest="infile",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        help="the filename to write the results to (e.g. output.txt)",
        type=str,
        dest="outfile",
    )

    return parser.parse_args()


def get_word_list(args) -> list:
    if args.infile:
        with open(args.infile, "r") as f:
            words = list(map(str.strip, f.readlines()))
    elif args.words:
        words = list(map(str.strip, args.words.split(",")))
    else:
        import sys
        import os

        print(
            "Invalid arguments. Please run the following command for a how-to instruction."
        )
        print(f"python3 {os.path.basename(__file__)} -h")
        sys.exit(1)

    return words


def preprocess_words(words):
    return list(map(lambda word: "-".join(word.split(" ")), words))


if __name__ == "__main__":
    args = create_parser()
    words = get_word_list(args)
    words = preprocess_words(words)
    base_url = "https://www.oxfordlearnersdictionaries.com/definition/english/"

    for word in words:
        print(f"Processing {word}...")
        page = check_output(f"curl -s {base_url + word}", shell=True)
        soup = BeautifulSoup(page, "html.parser")
        
