from concurrent import futures
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/"
HEADERS = requests.utils.default_headers()
HEADERS.update({"User-Agent": "Edge"})

NUM_THREADS = 10


def preprocess_words(words):
    """

    Preprocess words:
    -  Strip whitespaces at the begining and the end of the word/phrase
    -  Replace whitespaces within the word/phrase with dashes

    """
    words = list(map(str.strip, words))
    words = list(map(str.lower, words))
    return list(map(lambda word: "-".join(word.split(" ")), words))


def crawl_resource(word) -> str:
    """Get the web page of the word and parse it."""
    page = requests.get(BASE_URL + word, headers=HEADERS).text
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
        phon = soup.find_all(class_="phon")[1]
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


def run(wordlist: list):
    """Create a vocabulary list from the specified wordlist."""
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        # using map to cause to program to wait for all workers to complete
        # before continue
        results = list(executor.map(crawl_resource, wordlist))
    return ''.join(results)
