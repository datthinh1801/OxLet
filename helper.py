from subprocess import check_output
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/"
HEADERS = requests.utils.default_headers()
HEADERS.update({"User-Agent": "Edge"})


def preprocess_words(words):
    return list(map(lambda word: "-".join(word.split(" ")), words))


def crawl_resource(word) -> str:
    # page = check_output(f"curl -s -L {BASE_URL + word}", shell=True)
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
