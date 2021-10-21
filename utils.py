import json
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
        "uk_phon_class": "phons_br",
        "us_phon_class": "phons_n_am",
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
    -  Strip whitespaces at the beginning and the end of the word/phrase
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


async def parse_page(session: aiohttp.ClientSession, word: str, **kwargs) -> dict:
    """Crawl the source code and parse elements via given classes."""
    url = BASE_URL[kwargs['dict_type']] + word
    page = await fetch_html(url=url, session=session)
    soup = BeautifulSoup(page, "html.parser")

    result = dict()

    # extract headword
    try:
        result['word'] = soup.find(class_=kwargs['hw_class']).text
    except:
        return None

    # extract phonetic
    try:
        # extract NA phonetic
        uk = soup.find_all('div', kwargs['uk_phon_class'])[0]
        uk_phonetic = uk.find('span', 'phon').text
        uk_media = uk.find('div')['data-src-mp3']
        us = soup.find_all('div', kwargs['us_phon_class'])[0]
        us_phonetic = us.find('span', 'phon').text
        us_media = us.find('div')['data-src-mp3']
        result['phonetics'] = {
            'uk': {
                'phon': uk_phonetic,
                'media': uk_media,
            },
            'us': {
                'phon': us_phonetic,
                'media': us_media,
            }
        }
    except Exception as e:
        print(e)
        pass

    # extract word form
    try:
        result['word_form'] = soup.find(class_=kwargs['wf_class']).text
    except:
        pass

    sense = soup.find(class_=kwargs['sense_class'])
    # extract definition
    try:
        definition = sense.find(class_=kwargs['def_class'])
        if kwargs['dict_type'] == "cambridge":
            result['definition'] = definition.text.replace(':', '')
        else:
            result['definition'] = definition.text
    except:
        return None

    # extract example
    try:
        result['example'] = sense.find(class_=kwargs['ex_class']).text
    except:
        pass

    return result


async def crawl_resource(session: aiohttp.ClientSession, word: str) -> dict or None:
    """Get the web page of the word and parse it."""
    result = None
    for dictionary in DICT_PROFILES:
        result = await parse_page(session, word, **DICT_PROFILES[dictionary])
        if result is not None:
            break
    return result


async def run(wordlist: list):
    """Create a vocabulary list from the specified wordlist."""
    async with aiohttp.ClientSession(headers={"User-Agent": "Chrome"}) as session:
        tasks = []
        for word in wordlist:
            tasks.append(crawl_resource(session=session, word=word))
        results = await asyncio.gather(*tasks)
    return '\n\n'.join(results)


