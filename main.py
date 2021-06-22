import requests
import json

app_id = '6c4b0aaa'
app_key = '55a83148c8ad92dd31e3c312d845bb9a'
language = 'en-gb'

word_id = 'sustainable'
url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + \
    language + '/' + word_id.lower()

r = requests.get(url, headers=dict(app_id=app_id, app_key=app_key))

print(f"code {r.status_code}")
print(f"text {r.text}")
print(f"json {json.dumps(r.json())}")
