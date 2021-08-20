import asyncio

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

BASE_URL = {"oxford": "https://www.oxfordlearnersdictionaries.com/definition/english/",
            "cambridge": "https://dictionary.cambridge.org/dictionary/english/"}
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


def preprocess_words(words):
    """
    Preprocess words:
    -  Strip whitespaces at the begining and the end of the word/phrase
    -  Replace whitespaces within the word/phrase with dashes
    """
    words = list(map(str.strip, words))
    words = list(map(str.lower, words))
    return list(map(lambda word: "-".join(word.split(" ")), words))


async def fetch_html(url: str, session: ClientSession):
    """Fetch html from a given url."""
    resp = await session.get(url=url)
    html = await resp.text()
    return html


async def parse_page(session: aiohttp.ClientSession,
                     word: str,
                     **kwargs) -> str:
    """Crawl the source code and parse elements via given classes."""
    url = BASE_URL[kwargs['dict_type']] + word
    page = await fetch_html(url=url, session=session)
    soup = BeautifulSoup(page, "html.parser")

    # extract headword
    try:
        headword = soup.find(class_=kwargs['hw_class'])
        result = headword.text
    except:
        return None

    # extract phonetic
    try:
        # extract NA phonetic
        phon = soup.find_all(class_=kwargs['phon_class'])[1]
        result += f"\n({phon.text})"
    except:
        pass

    # extract word form
    try:
        word_form = soup.find(class_=kwargs['wf_class'])
        result += f"|({word_form.text}) "
    except:
        result += '|'
        pass

    sense = soup.find(class_=kwargs['sense_class'])
    # extract definition
    try:
        definition = sense.find(class_=kwargs['def_class'])
        if kwargs['dict_type'] == "cambridge":
            result += definition.text.replace(':', '')
        else:
            result += definition.text
    except:
        return None

    # extract example
    try:
        example = sense.find(class_=kwargs['ex_class'])
        result += "\ne.g. " + example.text
    except:
        pass

    return result


async def crawl_resource(session: aiohttp.ClientSession, word: str) -> str:
    """Get the web page of the word and parse it."""
    for dictionary in DICT_PROFILES:
        result = await parse_page(session, word, **DICT_PROFILES[dictionary])
        if result is not None:
            break
    else:
        result = ''
    return result


async def run(wordlist: list):
    """Create a vocabulary list from the specified wordlist."""
    async with aiohttp.ClientSession(headers={"User-Agent": "Chrome"}) as session:
        tasks = []
        for word in wordlist:
            tasks.append(crawl_resource(session=session, word=word))
        results = await asyncio.gather(*tasks)
    return '\n\n'.join(results)
