import json
import os
import requests

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
ORACLE_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-cards.json')
ORACLE_BULK_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-bulk.json')
NAMES_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-names.txt')
LEGEND_TOKEN_NAMES_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-legend-token-names.txt')
SETS_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-sets.json')
BASE_URL = 'http://api.scryfall.com/'
URI_KEY = 'download_uri'


def get_fetch_url(endpoint):
    url = f'{BASE_URL}bulk-data/{endpoint}'
    response = requests.get(url)
    if not response.ok:
        raise LookupError(response.status_code)
    obj = response.json()
    if not URI_KEY in obj:
        raise KeyError(f'Return object missing {URI_KEY}')
    return obj[URI_KEY]

def fetch_scryfall_oracle_cards():
    url = get_fetch_url('oracle-cards')
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    os.makedirs(os.path.dirname(ORACLE_OUT), exist_ok=True)
    with open(ORACLE_OUT, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

def fetch_scryfall_oracle_all():
    url = get_fetch_url('default_cards')
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    os.makedirs(os.path.dirname(ORACLE_OUT), exist_ok=True)
    with open(ORACLE_BULK_OUT, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

def fetch_card_names():
    url = f'{BASE_URL}catalog/card-names'
    r = requests.get(url)
    data: dict[str, list[str]] = r.json()
    os.makedirs(os.path.dirname(ORACLE_OUT), exist_ok=True)
    with open(NAMES_OUT, 'w') as f:
        f.write('\n'.join(sorted(set([
            name
            for card in data['data']
            for name in card.split(' // ')
        ]))))

def fetch_legend_tokens():
    url = f'{BASE_URL}cards/search?q=type=legendary and type=token'
    r = requests.get(url)
    data: dict[str, list[str]] = r.json()
    os.makedirs(os.path.dirname(ORACLE_OUT), exist_ok=True)
    with open(LEGEND_TOKEN_NAMES_OUT, 'w') as f:
        f.write('\n'.join(sorted(set([
            name
            for card in data['data']
            for name in card['name'].split(' // ')
        ]))))
    if data['has_more']:
        raise LookupError('We need to write more!')

def fetch_sets():
    url = f' {BASE_URL}sets/'
    r = requests.get(url)
    data: dict[str, list[str]] = r.json()
    os.makedirs(os.path.dirname(ORACLE_OUT), exist_ok=True)
    with open(SETS_OUT, 'w') as f:
        json.dump(data['data'], f, indent=4)
    if data['has_more']:
        raise LookupError('We need to write more!')


if __name__ == '__main__':
    fetch_scryfall_oracle_cards()
    fetch_scryfall_oracle_all()
    fetch_card_names()
    fetch_legend_tokens()
    fetch_sets()
