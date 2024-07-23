import json
import os
import sys
from mtg_parser import create_parsed_obj
from utils.file_ops import DATA, get_cards_by_set

def dump_it(obj: dict):
    return '\n'.join(['    ' + x for x in json.dumps(obj, indent=4).split('\n')])

def main(set_code):
    cards = get_cards_by_set(set_code)
    parsed_cards = [
        card_obj
        for card_objs in [create_parsed_obj(card) for card in cards]
        for card_obj in card_objs
    ]
    with open(os.path.join(DATA.CARD_JSON, set_code + '.json'), 'w') as f:
        json.dump(parsed_cards, f, indent=4)

if __name__ == '__main__':
    args = sys.argv
    set_code = args[-1]
    set_code = 'blc'
    main(set_code)
