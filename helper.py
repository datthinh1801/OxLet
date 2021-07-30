from concurrent import futures
import requests
from bs4 import BeautifulSoup


BASE_URL = {"oxford": "https://www.oxfordlearnersdictionaries.com/definition/english/",
            "cambridge": "https://dictionary.cambridge.org/dictionary/english/"}
HEADERS = requests.utils.default_headers()
HEADERS.update({"User-Agent": "Edge"})
DICT_PROFILES = {
    "oxford": {
        "dict_type": "oxford",
        "hw_class": "headword",
        "phon_class": "phon",
        "wf_class": "pos",
        "sense_class": "sense",
        "def_class": "def",
        "ex_class": "x"
    },
    "cambridge": {
        "dict_type": "cambridge",
        "hw_class": "dhw",
        "phon_class": "ipa dipa lpr-2 lpl-1",
        "wf_class": "pos dpos",
        "sense_class": "ddef_block",
        "def_class": "def ddef_d db",
        "ex_class": "eg deg"
    }
}

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


def parse_page(word, dict_type, hw_class, phon_class, wf_class, sense_class, def_class, ex_class) -> str:
    """Crawl the source code and parse elements via given classes."""
    page = requests.get(BASE_URL[dict_type] + word, headers=HEADERS).text
    soup = BeautifulSoup(page, "html.parser")

    # extract headword
    try:
        headword = soup.find(class_=hw_class)
        result = headword.text
    except:
        return None

    # extract phonetic
    try:
        # extract phonetic
        phon = soup.find_all(class_=phon_class)[1]
        result += f"\n({phon.text})"
    except:
        pass

    # extract word form
    try:
        word_form = soup.find(class_=wf_class)
        result += f"|({word_form.text}) "
    except:
        pass

    sense = soup.find(class_=sense_class)
    # extract definition
    try:
        definition = sense.find(class_=def_class)
        if dict_type == "cambridge":
            result += definition.text.replace(':', '')
        else:
            result += definition.text
    except:
        return None

    # extract example
    try:
        example = sense.find(class_=ex_class)
        result += "\ne.g. " + example.text
    except:
        pass

    # append delimiter between 2 words
    result += "\n\n"
    return result


def crawl_resource(word) -> str:
    """Get the web page of the word and parse it."""
    for dictionary in DICT_PROFILES:
        result = parse_page(word, **DICT_PROFILES[dictionary])
        if result is not None:
            break
    else:
        result = ''
    return result


def run(wordlist: list):
    """Create a vocabulary list from the specified wordlist."""
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        # using map to cause to program to wait for all workers to complete
        # before continue
        results = list(executor.map(crawl_resource, wordlist))
    return ''.join(results)
