import json
import os
import re
from nltk.tokenize import word_tokenize

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE_IN = os.path.join(DATA_DIR, 'out', 'oracles_text.ndjson')
DATA_FILE_OUT_ORACLE = os.path.join(DATA_DIR, 'out', 'oracle_only.txt')
DATA_FILE_OUT_NAME = os.path.join(DATA_DIR, 'out', 'name_only.txt')

IGNORE_NAMES = [
    "Turntimber Symbiosis // Turntimber, Serpentine Wood",
    "Kolvori, God of Kinship // The Ringhart Crest",
    "Invasion of Kaldheim // Pyre of the World Tree",
    "A-Cauldron Familiar"
]

CONTRACTIONS = {
    "aren't": "are not",
    "there's": "there is",
    "can't": "can not",
    "they'd": "they had; they would",
    "couldn't": "could not",
    "they'll": "they will",
    "didn't": "did not",
    "they're": "they are",
    "doesn't": "does not",
    "they've": "they have",
    "don't": "do not",
    "we'd": "we had",
    "hadn't": "had not",
    "we're": "we are",
    "hasn't": "has not",
    "we've": "we have",
    "haven't": "have not",
    "weren't": "were not",
    "he'd": "he had",
    "what'll": "what will",
    "he'll": "he will",
    "what're": "what are",
    "he's": "he is",
    "what's": "what is",
    "I'd": "I had",
    "what've": "what have",
    "I'll": "I will",
    "where's": "where is",
    "I'm": "I am",
    "who'd": "who had",
    "I've": "I have",
    "who'll": "who will",
    "isn't": "is not",
    "who're": "who are",
    "let's": "let us",
    "who's": "who is",
    "mightn't": "might not",
    "who've": "who have",
    "mustn't": "must not",
    "won't": "will not",
    "shan't": "shall not",
    "wouldn't": "would not",
    "she'd": "she had",
    "you'd": "you had",
    "she'll": "she will",
    "you'll": "you will",
    "she's": "she is",
    "you're": "you are",
    "shouldn't": "should not",
    "you've": "you have",
    "that's": "that is",
    "it's": "it is"
}

def alter_oracle(card):
    if not card:
        return
    if not card['oracle']:
        return card

    if card['name'] in (
        "Mu Yanling, Sky Dancer",
    ):
        # Currently have an issue parsing the island emblem, so just return at the moment
        return

    to_parse = card['oracle']

    name = card.get('card')

    for i, name in enumerate(card['name'].split(' // ')):
        to_parse = to_parse.replace(name[2:] if name.startswith('A-') else name, f'~{i if i else ""}')
        if ',' in name:
            to_parse = to_parse.replace(
                name.split(',')[0][2:] if name.startswith('A-') else name.split(',')[0], f'~{i if i else ""}'
            )

    if 'A-~' in to_parse:
        to_parse = to_parse.replace('A-~', '~')

    to_parse = re.sub(r' {0,1}\([^)]*\)', '', to_parse)
    to_parse = to_parse.split('\n')

    # Parse out any subs
    subs = []
    for each in to_parse:
        for k,v in CONTRACTIONS.items():
            each = each.replace(k,v)
        tokens = word_tokenize(each)
        sub = []
        is_sub = False
        for token in tokens:
            if token == '``':
                token = '"'
            if token == "''":
                token = '"'
            if '"' in token:
                if not is_sub:
                    is_sub = True
                    token = token[1:]
                elif is_sub:
                    is_sub = False
                    token = token[:-1]
                    if token:
                        if token in ":,'.".split():
                            if not sub:
                                sub.append('')
                            sub[-1] += token
                        else:
                            sub.append(token)
                    joined = ' '.join(sub)
                    # for k,v in CONTRACTIONS.items():
                    #     joined = joined.replace(v, k)
                    if '{' in joined:
                        joined = re.sub(r'\{\s*(.*?)\s*\}', r'{\1}', joined)
                    if '} {' in joined:
                        joined = joined.replace('} {', '}{')
                    if '[' in joined:
                        joined = re.sub(r'\[\s*(.*?)\s*\]', r'[\1]', joined)
                    subs.append(joined)
                    sub = []
            if is_sub and token:
                if token in ":,'.":
                    if not sub:
                        sub.append('')
                    sub[-1] += token
                else:
                    sub.append(token)

    card['oracle'] = to_parse + subs

    # not sure what caused this bug, but this is the easiest fix for now
    for i in range(len(card['oracle'])):
        card['oracle'][i] = card['oracle'][i].replace(" '", "'")

    return card


def main():
    with open(DATA_FILE_IN) as f:
        # data = [
        #     alter_oracle({
        #         'oracle': 'This is "testing it"',
        #         'name': 'Test Card'
        #     })
        # ] +
        data = [alter_oracle(json.loads(x)) for x in f.read().split('\n') if x]

    with open(DATA_FILE_OUT_ORACLE, 'w') as f:
        for x in data:
            if not x:
                continue
            if x['name'] in IGNORE_NAMES:
                continue
            for y in x['oracle']:
                f.write(y + '\n')

    names = [x['card'] for x in data if x]
    names.sort()
    with open(DATA_FILE_OUT_NAME, 'w') as f:
        for x in names:
            f.write(x + '\n')

if __name__ == '__main__':
    main()
