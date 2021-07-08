import argparse
from helper import *


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


if __name__ == "__main__":
    args = create_parser()
    words = get_word_list(args)
    words = preprocess_words(words)

    # empty the outfile first
    with open(args.outfile, "w") as f:
        pass
    with open(args.outfile, "ab") as outfile:
        for word in words:
            print(f"Processing {word}...")
            result = crawl_resource(word)
            # append the result to file
            outfile.write(result.encode())
