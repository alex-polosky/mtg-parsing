from hashlib import md5
import json
import os
import pickle
from mtg_parser import ScryfallCard

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE = os.path.join(DATA_DIR, 'scryfall', 'oracle-cards.json')
DATA_OUT = os.path.join(DATA_DIR, 'bin', 'scry-cards.bin')


def main():
    with open(DATA_FILE) as f:
        data = [ScryfallCard(x) for x in json.load(f)]
    data = {
        card.oracle_id: card
        for card in data
    }
    b = pickle.dumps(data)
    m = md5(b).hexdigest()
    with open(DATA_OUT, 'wb') as f:
        f.write(b)
    with open(DATA_OUT + '.md5', 'w') as f:
        f.write(m)


if __name__ == '__main__':
    main()
