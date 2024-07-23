from hashlib import md5
import json
import os
import pickle
from mtg_parser import ScryfallCard
from utils.file_ops import DATA


def main():
    with open(DATA.ORACLE_CARDS) as f:
        data = [ScryfallCard(x) for x in json.load(f)]
    data = {
        card.oracle_id: card
        for card in data
    }
    b = pickle.dumps(data)
    m = md5(b).hexdigest()
    with open(DATA.BIN_ORACLE, 'wb') as f:
        f.write(b)
    with open(DATA.BIN_ORACLE + '.md5', 'w') as f:
        f.write(m)


if __name__ == '__main__':
    main()
