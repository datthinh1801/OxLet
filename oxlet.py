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

    # empty the outfile first
    with open(args.outfile, "w") as f:
        pass
    with open(args.outfile, "ab") as outfile:
        for word in words:
            print(f"Processing {word}...")
            page = check_output(f"curl -s -L {base_url + word}", shell=True)
            soup = BeautifulSoup(page, "html.parser")
            sense = soup.find(class_="sense")

            result = ""

            # extract headword
            headword = soup.find(class_="headword")
            result += headword.text + "\n"

            try:
                # extract phonetic
                phon = soup.find(class_="phon")
                result += f"({phon.text})" + "|"
            except:
                print("\tNo phonetic was found!")
            # extract definition
            definition = sense.find(class_="def")
            result += definition.text + "\n"

            try:
                # extract example
                example = sense.find(class_="examples").find_next("li")
                result += "e.g. " + example.text
            except:
                print("\tNo example was found!")

            # append delimiter between 2 words
            result += "\n\n"

            # append the result to file
            outfile.write(result.encode())
