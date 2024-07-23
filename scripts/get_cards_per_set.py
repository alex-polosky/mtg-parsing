import json
import os
from utils.scryfall_card import ScryfallCard

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE = os.path.join(DATA_DIR, 'scryfall', 'oracle-bulk.json')
DATA_FILE_OUT = os.path.join(DATA_DIR, 'out', 'cards_per_set.json')


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)
    sets = {}
    for card_json in data:
        card = ScryfallCard(card_json)
        if card.set not in sets:
            sets[card.set] = []
        id_ = str(card.oracle_id)
        if id_ not in sets[card.set]:
            sets[card.set].append(id_)
    with open(DATA_FILE_OUT, 'w') as f:
        json.dump(sets, f, indent=4)


if __name__ == '__main__':
    main()
