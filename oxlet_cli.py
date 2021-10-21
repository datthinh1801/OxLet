import argparse
import asyncio
import os
import sys

import utils
import anki


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

    parser.add_argument(
        "--anki",
        help="add new vocabularies to Anki automatically",
        action='store_true',
        dest="anki",
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
    # fix Windows-specific exception:
    # RuntimeError: Event loop is closed.
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    args = create_parser()
    words = get_word_list(args)
    words = utils.preprocess_words(words)

    if args.anki:
        try:
            asyncio.run(anki.run(words))
        except OSError:
            print("[-] Make sure Anki is running and AnkiConnect plugin is installed!")
    else:
        results = asyncio.run(utils.run(words))
        if args.outfile:
            with open(args.outfile, "wb") as outfile:
                outfile.write(results.encode())
        else:
            print(results)
