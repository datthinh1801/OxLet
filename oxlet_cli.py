import sys
import os
import argparse

import helper


def create_parser():
    """Create a parser and parse CLI arguments."""
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
    """Get words from a wordlist."""
    if args.infile:
        with open(args.infile, "r") as wordlist:
            words = list(map(str.strip, wordlist.readlines()))
    elif args.words:
        words = list(map(str.strip, args.words.split(",")))
    else:
        print(
            "Invalid arguments. Please run the following command for a how-to instruction."
        )
        print(f"python3 {os.path.basename(__file__)} -h")
        sys.exit(1)

    return words


if __name__ == "__main__":
    args = create_parser()
    words = get_word_list(args)
    words = helper.preprocess_words(words)

    with open(args.outfile, "wb") as outfile:
        results = helper.run(words)
        outfile.write(results.encode())
