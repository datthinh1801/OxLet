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
        "phon_text": "phon",
        "phon_media": "data-src-mp3",
        "wf_class": "pos",
        "sense_class": "sense",
        "def_class": "def",
        "ex_class": "x"
    },
    "cambridge": {
        "dict_type": "cambridge",
        "hw_class": "dhw",
        "uk_phon_class": "uk dpron-i",
        "us_phon_class": "us dpron-i",
        "phon_text": "pron dpron",
        "phon_media": "audio/mpeg",
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

    # print(soup.find_all(class_='us')[0].find('source', type='audio/mpeg')['src'])
    result['phonetics'] = {
        'uk': {
            'phon': '',
            'media': '',
        },
        'us': {
            'phon': '',
            'media': '',
        }
    }
    # extract phonetic
    try:
        # extract NA phonetic
        if kwargs['dict_type'] == 'oxford':
            uk = soup.find_all('div', kwargs['uk_phon_class'])[0]
            result['phonetics']['uk']['phon'] = uk.find('span', 'phon').text
            result['phonetics']['uk']['media'] = uk.find('div')['data-src-mp3']

            us = soup.find_all('div', kwargs['us_phon_class'])[0]
            result['phonetics']['us']['phon'] = us.find('span', 'phon').text
            result['phonetics']['us']['media'] = us.find('div')['data-src-mp3']
        # elif kwargs['dict_type'] == 'cambridge':
        else:
            uk = soup.find_all(class_=kwargs['uk_phon_class'])[0]
            result['phonetics']['uk']['phon'] = uk.find(class_=kwargs['phon_text']).text
            result['phonetics']['uk']['media'] = uk.find('source', type=kwargs['phon_media'])['src']
            us = soup.find_all(class_=kwargs['us_phon_class'])[0]
            result['phonetics']['us']['phon'] = us.find(class_=kwargs['phon_text']).text
            result['phonetics']['us']['media'] = us.find('source', type=kwargs['phon_media'])['src']

    except:
        pass

    # extract word form
    try:
        result['word_form'] = soup.find(class_=kwargs['wf_class']).text
    except:
        result['word_form'] = ''

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
        result['example'] = ''

    return result


async def crawl_resource(session: aiohttp.ClientSession, word: str) -> dict or None:
    """Get the web page of the word and parse it."""
    result = None
    for dictionary in DICT_PROFILES:
        result = await parse_page(session, word, **DICT_PROFILES[dictionary])
        if result is not None:
            break
    return result


def parse_word_dict(data) -> str:
    if data is None:
        return ''

    result = data['word']
    if data['phonetics']['us']['phon']:
        result += '\n' + data['phonetics']['us']['phon']
    result += '|'
    if data['word_form']:
        result += f"({data['word_form']})"
    if data['example']:
        result += '\n' + data['example']
    return result


async def run(wordlist: list, return_str=True):
    """Create a vocabulary list from the specified wordlist."""
    async with aiohttp.ClientSession(headers={"User-Agent": "Chrome"}) as session:
        tasks = []
        for word in wordlist:
            tasks.append(crawl_resource(session=session, word=word))
        results = await asyncio.gather(*tasks)
    if return_str:
        return '\n\n'.join(list(map(parse_word_dict, results)))
    return results
