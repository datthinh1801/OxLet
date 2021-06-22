from pprint import pprint
import requests
import json
import argparse

# Create a parser
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--words',
                    nargs='?',
                    help="a list of words/phrases separated by commas (e.g. sustainable, take a toll)",
                    type=str,
                    dest='words')
parser.add_argument('-f', '--file',
                    nargs='?',
                    help='the name of the file to read from (e.g. newwords.txt)',
                    type=str,
                    dest="infile")
parser.add_argument('-o', '--output',
                    nargs='?',
                    help="the filename to write the results to (e.g. output.txt)",
                    type=str,
                    dest='outfile')

args = parser.parse_args()

if args.infile:
    with open(args.infile, 'r') as f:
        words = list(map(str.strip, f.readlines()))
elif args.words:
    words = list(map(str.strip, args.words.split(',')))
else:
    import sys
    import os

    print("Invalid arguments. Please run the following command for a how-to instruction.")
    print(f"python3 {os.path.basename(__file__)} -h")
    sys.exit(1)

# API setup
app_id = '6c4b0aaa'
app_key = '55a83148c8ad92dd31e3c312d845bb9a'
language = 'en-gb'


with open(args.outfile, 'w') as f:
    for word in words:
        print(f"Looking up {word}...")
        # acquire data from oxford
        url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + \
            language + '/' + word.lower()

        r = requests.get(url, headers=dict(app_id=app_id, app_key=app_key))

        # Extract the first result
        try:
            result = r.json()['results'][0]
        except:
            print("Failed on acquiring result.")
            continue

        # Extract word id
        try:
            word_id = result['id']
        except:
            print("Failed on acquiring word_id.")
            continue

        # Extract the first lexical entry
        try:
            lexical_entry = result['lexicalEntries'][0]['entries'][0]
        except:
            print("Failed on acquiring lexical_entry.")

        # Extract the first definition
        try:
            definition = lexical_entry['senses'][0]['definitions'][0]
        except:
            print("Failed on acquiring definition.")
            continue

        # Extract the first example
        try:
            example = lexical_entry['senses'][0]['examples'][0]['text']
        except:
            print("Failed on acquiring example.")
            continue

        # write result to file
        try:
            string_to_write = f"{word_id}|{definition}\\{example}"
            f.write(string_to_write)
            f.write('\n')
        except:
            print("Failed!")
            continue
        print("Succeeded!")
