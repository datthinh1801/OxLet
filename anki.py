import asyncio
import json
from aiohttp import ClientSession

from utils import crawl_resource


async def send_to_anki(session: ClientSession, data: dict):
    return await session.post(url='http://localhost:8765', data=json.dumps(data).encode('utf-8'))


async def create_new_note(session: ClientSession, word: str):
    result = await crawl_resource(session, word)
    if result is None:
        return None

    new_card = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Default",
                "modelName": "English (by datthinh1801)",
                "fields": {
                    "Word": result['word'],
                    "Phonetic": result['phonetics']['us']['phon'],
                    "Word form": result['word_form'],
                    "Definition": result['definition']
                },
                'options': {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                },
                "tags": ["english_vocab"],
                "audio": [{
                    "url": result['phonetics']['us']['media'],
                    "filename": f'{result["word"]}_us.mp3',
                    "fields": ["Phonetic"]
                }]
            }
        }
    }
    return await send_to_anki(session, new_card)


async def check_model_exist(session: ClientSession) -> bool:
    model_name = 'English (by datthinh1801)'
    modelnames_request = {"action": "modelNames", "version": 6}
    resp = await send_to_anki(session, modelnames_request)
    resp_json = json.loads(await resp.text())
    return resp_json['error'] is None and 'English (by datthinh1801)' in resp_json['result']


async def create_new_model(session: ClientSession):
    if await check_model_exist(session):
        # await update_model_template(session)
        return None

    new_model = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": 'English (by datthinh1801)',
            "inOrderFields": ["Word", "Phonetic", "Word form", "Definition"],
            "isCloze": False,
            "cardTemplates": [
                {
                    "Name": "Basic type",
                    "Front": "{{Word}}<br>{{Phonetic}}",
                    "Back": "{{Word}}<br>{{Phonetic}}<hr id=answer>{{Word form}}<br>{{Definition}}"
                },
                {
                    "Name": "Basic reverse type",
                    "Front": "{{Word form}}<br>{{Definition}}",
                    "Back": "{{Word form}}<br>{{Definition}}<hr id=answer>{{Word}}<br>{{Phonetic}}"
                },
                {
                    "Name": "Listening type",
                    "Front": "{{Phonetic}}",
                    "Back": "{{Word}}<br>{{Phonetic}}<hr id=answer>{{Word form}}<br>{{Definition}}"
                }
            ]
        }
    }
    # Sometimes, a ConnectionResetError occurs
    return await send_to_anki(session, new_model)


async def update_model_template(session: ClientSession):
    new_model_template = {
        'action': 'updateModelTemplates',
        'version': 6,
        'params': {
            'model': {
                'name': 'English (by datthinh1801)',
                'templates': {
                    "Basic type": {
                        "Front": "{{Word}}<br>{{Phonetic}}",
                        "Back": "{{Word}}<br>{{Phonetic}}<hr id=answer>{{Word form}}<br>{{Definition}}"
                    },
                    "Basic reverse type": {
                        "Front": "{{Word form}}<br>{{Definition}}",
                        "Back": "{{Word form}}<br>{{Definition}}<hr id=answer>{{Word}}<br>{{Phonetic}}"
                    },
                    "Listening type": {
                        "Front": "{{Phonetic}}",
                        "Back": "{{Word}}<br>{{Phonetic}}<hr id=answer>{{Word form}}<br>{{Definition}}"
                    }
                }
            }
        }
    }
    resp = await send_to_anki(session, new_model_template)
    print(await resp.text())


async def run(wordlist: list):
    async with ClientSession(headers={"User-Agent": "Chrome"}) as session:
        tasks = []
        await create_new_model(session)
        for word in wordlist:
            tasks.append(create_new_note(session, word))
        await asyncio.gather(*tasks)
    print('[+] Done.')


if __name__ == '__main__':
    asyncio.run(run(['imperceptible', 'susceptible']))
