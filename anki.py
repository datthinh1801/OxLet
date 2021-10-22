import requests
import json

from utils import crawl_resource


def send_to_anki(session: requests.Session, data: dict):
    return session.post('http://localhost:8765', data=data)


def create_new_note(session: requests.Session, word: str):
    result = crawl_resource(session, word)
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
                    "Definition": result['definition'],
                    "Example": result['example']
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
    return send_to_anki(session, new_card)


def check_model_exist(session: requests.Session) -> bool:
    modelnames_request = {"action": "modelNames", "version": 6}
    resp = send_to_anki(session, modelnames_request)
    resp_json = json.loads(resp.text)
    return resp_json['error'] is None and 'English (by datthinh1801)' in resp_json['result']


def create_new_model(session: requests.Session):
    if check_model_exist(session):
        return None

    new_model = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": 'English (by datthinh1801)',
            "inOrderFields": ["Word", "Phonetic", "Word form", "Definition", "Example"],
            "isCloze": False,
            "cardTemplates": [
                {
                    "Name": "Basic type",
                    "Front": "{{Word}}<br>{{Phonetic}}",
                    "Back": """{{Word}}
                                <br>
                                {{Phonetic}}
                                <hr id=answer>
                                {{Word form}}
                                <br>
                                {{Definition}}
                                <br>
                                e.g. {{Example}}"""
                },
                {
                    "Name": "Basic reverse type",
                    "Front": "{{Word form}}<br>{{Definition}}",
                    "Back": """{{Word form}}
                                <br>
                                {{Definition}}
                                <hr id=answer>
                                {{Word}}
                                <br>
                                {{Phonetic}}"""
                },
                {
                    "Name": "Listening type",
                    "Front": "{{Phonetic}}",
                    "Back": """{{Word}}
                                <br>
                                {{Phonetic}}
                                <hr id=answer>
                                {{Word form}}
                                <br>
                                {{Definition}}
                                <br>
                                e.g. {{Example}}"""
                }
            ]
        }
    }
    return send_to_anki(session, new_model)


def update_model_template(session: requests.Session):
    new_model_template = {
        'action': 'updateModelTemplates',
        'version': 6,
        'params': {
            'model': {
                'name': 'English (by datthinh1801)',
                'templates': {
                    "Basic type": {
                        "Front": "{{Word}}<br>{{Phonetic}}",
                        "Back": """{{Word}}
                                <br>
                                {{Phonetic}}
                                <hr id=answer>
                                {{Word form}}
                                <br>
                                {{Definition}}
                                <br>
                                e.g. {{Example}}"""
                    },
                    "Basic reverse type": {
                        "Front": "{{Word form}}<br>{{Definition}}",
                        "Back": """{{Word form}}
                                    <br>
                                    {{Definition}}
                                    <hr id=answer>
                                    {{Word}}
                                    <br>
                                    {{Phonetic}}"""
                    },
                    "Listening type": {
                        "Front": "{{Phonetic}}",
                        "Back": """{{Word}}
                                    <br>
                                    {{Phonetic}}
                                    <hr id=answer>
                                    {{Word form}}
                                    <br>
                                    {{Definition}}"""
                    }
                }
            }
        }
    }
    resp = send_to_anki(session, new_model_template)
    print(resp.text)


def run(wordlist: list):
    with requests.Session() as session:
        print(send_to_anki(session, {'action': 'deckNames', 'version': 6}))
    print('[+] Done.')


if __name__ == '__main__':
    run(['imperceptible'])
