import json
import os
import sys
from types import FrameType
from mtg_parser import oracle_parser
from utils.file_ops import DATA, get_cards_by_set

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# def get_traceback(ex: Exception):
#     while ex.__traceback__.tb_next:
#         tb = 

def add_ex(frame: FrameType, depth: int):
    return {
        f'code{depth}': f'{frame.f_code.co_filename.replace(BASE_DIR, '')}:{frame.f_code.co_name}:{frame.f_lineno}',
    }

def parse_or_err(card, face_i=0):
    is_exception = False
    try:
        parsed = oracle_parser(card, face_i)
    except Exception as ex:
        parsed = {
            'ex': f'[{type(ex).__name__}] {ex.args[0] if ex.args else ""}'
        }

        tb = ex.__traceback__
        depth = 0
        while tb:
            parsed.update(add_ex(tb.tb_frame, depth))
            depth += 1
            tb = tb.tb_next

        is_exception = True
    return parsed, is_exception

def dump_it(obj: dict):
    return '\n'.join(['    ' + x for x in json.dumps(obj, indent=4).split('\n')])

def main(set_code):
    cards = get_cards_by_set(set_code)
    card_count = len(cards)
    with open(os.path.join(DATA.CARD_JSON, set_code + '.json'), 'w') as f:
        f.write('[\n')
        for card_i, card in enumerate(cards):
            obj = {
                'oracle_id': str(card.oracle_id),
                'face_id': 0,
                'name': card.name,
                'type_line': card.type_line,
                'layout': card.layout,
                'oracle_text': card.oracle_text,
                'colors': card.colors,
                'color_identity': card.color_identity,
                'color_indicator': card.color_indicator,
                'cmc': card.cmc,
                'mana_cost': card.mana_cost,
                'power': card.power,
                'defense': card.defense,
                'loyalty': card.loyalty,
            }

            if card.card_faces:
                objs = []
                for face_id, card_face in enumerate(card.card_faces):
                    objs.append(obj.copy())
                    objs[-1]['face_id'] = face_id + 1
                    for key in obj.keys():
                        if key in ('oracle_id', 'face_id'):
                            continue
                        if (attr := getattr(card_face, key, None)):
                            objs[-1][key] = attr
                    parsed, is_exception = parse_or_err(card, face_id + 1)
                    objs[-1]['parsed' if not is_exception else 'except'] = parsed
                    f.write(dump_it(objs[-1]))
                    if face_id < len(card.card_faces) - 1:
                        f.write(',\n')
            else:
                parsed, is_exception = parse_or_err(card)
                obj['parsed' if not is_exception else 'except'] = parsed
                f.write(dump_it(obj))

            if card_i < card_count - 1:
                f.write(',')

            f.write('\n')

        f.write(']')


if __name__ == '__main__':
    args = sys.argv
    set_code = args[-1]
    set_code = 'blc'
    main(set_code)
