import json
import os
import sys
from scripts.extract_oracle_text import IGNORE_NAMES, alter_oracle, export as export_extract
from scripts.generalize_oracle_text import generalize_oracle
from scripts.piece_out_oracle_text import get_datas
from utils.file_ops import DATA, get_cards_by_set

DECIMATE_THE_DECIMAL = True


def main(set_code):
    cards = get_cards_by_set(set_code)
    DIR = os.path.join(DATA.ANALYSIS, set_code)
    os.makedirs(DIR, exist_ok=True)

    cards_shifted = []
    for card in cards:
        obj = {
            'name': card.name,
            'oracle': card.oracle_text
        }
        if card.card_faces:
            for face in card.card_faces:
                objf = obj.copy()
                objf['oracle'] = face.oracle_text
                cards_shifted.append(objf)
        else:
            cards_shifted.append(obj)

    oracle_only = [alter_oracle(card) for card in cards_shifted]
    export_extract(oracle_only, os.path.join(DIR, 'oracle_only.txt'))

    generalized = [
        generalize_oracle(text, i)
        for i, oracle_text in enumerate([
            line
            for card in oracle_only
            if card and not card['name'] in IGNORE_NAMES
            for line in card['oracle']
            if line
        ])
        if oracle_text
        for text in (oracle_text.split('. ') if DECIMATE_THE_DECIMAL else [oracle_text])
    ]
    generalized = sorted(list(set(generalized)))
    with open(os.path.join(DIR, 'oracle_generalized.txt'), 'w') as f:
        f.write('\n'.join(generalized))

    (abilities, costs, oracles) = get_datas(generalized)
    with open(os.path.join(DIR, 'abilities.txt'), 'w') as f:
        f.write('\n'.join(abilities))
    with open(os.path.join(DIR, 'costs.txt'), 'w') as f:
        f.write('\n'.join(costs))
    with open(os.path.join(DIR, 'texts.txt'), 'w') as f:
        f.write('\n'.join(oracles))


if __name__ == '__main__':
    args = sys.argv
    set_code = args[-1]
    set_code = 'blc'
    main(set_code)
