import os
import requests

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE_OUT = os.path.join(DATA_DIR, 'scryfall', 'oracle-cards.json')
BASE_URL = 'http://api.scryfall.com/'
URI_KEY = 'download_uri'


def get_fetch_url():
    url = f'{BASE_URL}bulk-data/oracle-cards'
    response = requests.get(url)
    if not response.ok:
        raise LookupError(response.status_code)
    obj = response.json()
    if not URI_KEY in obj:
        raise KeyError(f'Return object missing {URI_KEY}')
    return obj[URI_KEY]

def fetch_scryfall():
    url = get_fetch_url()
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    os.makedirs(os.path.dirname(DATA_FILE_OUT), exist_ok=True)
    with open(DATA_FILE_OUT, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


if __name__ == '__main__':
    fetch_scryfall()
