from hashlib import md5
import json
import os
import pickle
from uuid import UUID
# from mtg_parser import ScryfallCard

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'))

class DATA:
    ORACLE_CARDS = os.path.join(DATA_DIR, 'scryfall', 'oracle-cards.json')
    ORACLE_BULK = os.path.join(DATA_DIR, 'scryfall', 'oracle-bulk.json')
    NAMES_ONLY = os.path.join(DATA_DIR, 'scryfall', 'oracle-names.txt')
    LEGEND_TOKEN_NAMES = os.path.join(DATA_DIR, 'scryfall', 'oracle-legend-token-names.txt')
    SETS = os.path.join(DATA_DIR, 'scryfall', 'oracle-sets.json')
    IDS_BY_SET = os.path.join(DATA_DIR, 'out', 'cards_per_set.json')
    BIN_ORACLE = os.path.join(DATA_DIR, 'bin', 'scry-cards.bin')
    ORACLE_TEXT = os.path.join(DATA_DIR, 'out', 'oracles_text.ndjson')
    ONLY_ORACLE = os.path.join(DATA_DIR, 'out', 'oracle_only.txt')
    # ONLY_NAME = os.path.join(DATA_DIR, 'out', 'name_only.txt')
    BIN_REGEX = os.path.join(DATA_DIR, 'bin', 'regex.bin')
    ORACLE_GENERALIZE = os.path.join(DATA_DIR, 'out', 'oracle_generalized.txt')
    ORACLE_ONLY_ABILITY = os.path.join(DATA_DIR, 'out', 'oracle_gen_ability.txt')
    ORACLE_ONLY_COST = os.path.join(DATA_DIR, 'out', 'oracle_gen_cost.txt')
    ORACLE_ONLY_GEN = os.path.join(DATA_DIR, 'out', 'oracle_gen_text.txt')
    ANALYSIS = os.path.join(DATA_DIR, 'analysis')
    CARD_JSON = os.path.join(DATA_DIR, 'cards')

_ORACLE: dict[str, any] = None
_SETS: dict[str, list[str]] = None

def get_cards():
    global _ORACLE
    if not _ORACLE:
        with open(DATA.BIN_ORACLE, 'rb') as f:
            b = f.read()
        with open(DATA.BIN_ORACLE + '.md5') as f:
            m = f.read()
        assert m == md5(b).hexdigest()
        _ORACLE = pickle.loads(b)
    return list(_ORACLE.values())

def get_cards_by_set(set: str):
    global _ORACLE, _SETS
    if not _SETS:
        with open(DATA.IDS_BY_SET) as f:
            _SETS = json.load(f)

    if set not in _SETS:
        raise KeyError(f'Unknown set: {set}')

    if not _ORACLE:
        with open(DATA.BIN_ORACLE, 'rb') as f:
            b = f.read()
        with open(DATA.BIN_ORACLE + '.md5') as f:
            m = f.read()
        assert m == md5(b).hexdigest()
        _ORACLE = pickle.loads(b)

    return [
        _ORACLE.get(UUID(id_))
        for id_ in _SETS[set]
    ]
