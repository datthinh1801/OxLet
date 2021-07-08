from subprocess import check_output
from bs4 import BeautifulSoup
import argparse

BASE_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/"


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


def crawl_resource(word) -> str:
    page = check_output(f"curl -s -L {BASE_URL + word}", shell=True)
    soup = BeautifulSoup(page, "html.parser")
    sense = soup.find(class_="sense")

    result = ""

    # extract headword
    try:
        headword = soup.find(class_="headword")
        result += headword.text
    except:
        return word + "\n\n"

    try:
        # extract phonetic
        phon = soup.find(class_="phon")
        result += f"\n({phon.text})"
    except:
        pass

    result += "|"

    # extract word form
    try:
        word_form = soup.find(class_="pos")
        result += f"({word_form.text}) "
    except:
        pass

    # extract definition
    try:
        definition = sense.find(class_="def")
        result += definition.text
    except:
        return word + "\n\n"

    try:
        # extract example
        example = sense.find(class_="examples").find_next("li")
        result += "\ne.g. " + example.text
    except:
        pass

    # append delimiter between 2 words
    result += "\n\n"
    return result


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