import os
import pickle
import re
from nltk.tokenize import word_tokenize

from mtg_types.abilities import abilities
from mtg_types.keywords import keywords
from mtg_types.types_ import types, super_types, card_types, role_tokens

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_REGEX = os.path.join(DATA_DIR, 'bin', 'regex.bin')
DATA_REGEX_MD5 = '0c37e7e18a7edd3c9bdcaefba1f318b0'
DATA_FILE_ORACLE = os.path.join(DATA_DIR, 'out', 'oracle_only.txt')
DATA_FILE_NAME = os.path.join(DATA_DIR, 'out', 'name_only.txt')
DATA_FILE_OUT = os.path.join(DATA_DIR, 'out', 'oracle_generalized.txt')

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


# I implemented this because loading all of these regexs was taking more than several minutes
if not os.path.exists(DATA_REGEX):
    def escape_re(s):
        for z in '\\.+*?^$()[]{}|':
            s = s.replace(z, f'\\{z}')
        return s

    with open(DATA_FILE_NAME) as f:
        # Due to possible conflicts, ignore 1 word cards for right now
        NAMES = [
            escape_re(x)
            for x in f.read().split('\n')
            if x and len(x.split()) > 1
        ]

    class RE:
        SPACING = re.compile(r'(?<! )—(?! )')
        COST = re.compile(r'((?:{(?:S|W|U|B|R|G|C|\d|X|Y|P|\/){1,3}})+)')
        ABILITY_PATTERNS =  {
            'ABILITY': [re.compile(rf'(^| )(?:{"|".join(abilities)})(?=$| |,|\.|;)', re.IGNORECASE)],
            'KEYWORD': [re.compile(rf'(^| )(?:{"|".join(keywords)})(?=$| |,|\.|;)', re.IGNORECASE)],
            'X_WALK': [re.compile(rf'(^| )\b(?:desert|plains|island|swamp|forest|mountain)walk\b', re.IGNORECASE)],
            'LAND_CYCLING': [re.compile(rf'(^| )\b(?:desert|plains|island|swamp|forest|mountain|basic land)cycling\b', re.IGNORECASE)]
        }
        ABILITY_DIGIT_MATCH = re.compile(r'^ \d(?=$| |,|\.)')
        STEP_PHASE = re.compile(r'\b(?!and\b|as\b|this\b)\w+ (?:phase|step)(?:s)?\b')
        CHOOSE_ONE = re.compile(r"choose (?:\w|\d|\s|')+ —", re.IGNORECASE)
        IMPLICIT_ABILITY = re.compile(r'((?<!KEYWORD)(?<!ABILITY)(?<!\d)(?<!MANA)) —', re.IGNORECASE)
        ROMANS = re.compile(r'^((?:\b[IVXLCDM]+\b(?:, \b[IVXLCDM]+\b)*))(?: —)')
        PW_ABILITY = re.compile(r'^((?:\[)?(?:\+|−|-){0,1}(?:\d{1,2}|X)(?:\])?):')
        CLASS_LEVEL = re.compile(r'^LEVEL \d{1,2}(?:-\d{1,2}){0,1}\+{0,1}')
        PT = re.compile(r'(?:\+|-){0}(?:\d{1,3}|\*|X|Y)\/(?:\+|-){0}(?:\d{1,3}|\*|X|Y)')
        PT_MOD = re.compile(r'(?:\+|-){1}(?:\d{1,3}|\*|X|Y)\/(?:\+|-){1}(?:\d{1,3}|\*|X|Y)')
        D20 = re.compile(r'^(?:\d+|\d+ — \d+) \|')
        BASIC_DIGITS = re.compile(r'\b(?<!~)\d+\b')
        NAMED = re.compile(rf'\b(?:{"|".join(NAMES)})\b', re.IGNORECASE)
        SUB_TYPES = re.compile(rf'\b(?:non|non-)?(?:{'|'.join([
            escape_re(sub_type)
            for subs in types.values()
            for sub_type in subs
        ])})\b', re.IGNORECASE)
        CARD_TYPES = re.compile(rf'\b(?:non|non-)?(?:{'|'.join(card_types)})\b', re.IGNORECASE)
        SUPER_TYPES = re.compile(rf'\b(?:non|non-)?(?:{'|'.join(super_types)})\b', re.IGNORECASE)
        ROLES = re.compile(rf'\b(?:{"|".join(role_tokens)})\b(?= role token)', re.IGNORECASE)
        POSSESSIVE = re.compile(r'''(?<!it|It)'(?:s| )\b''')
        ENERGY_TOKEN = re.compile(r'''(?:ENERGY)+''')
        # CAP_WORDS = re.compile(r'(?<!^)(?<!: )(?<!\. )(?<!— )(?<!• )[A-Z][a-z]+')

    _ = {}
    for k, r in vars(RE).items():
        if k.startswith('_'):
            continue
        _[k] = r
    _redump = pickle.dumps(_)
    from hashlib import md5 as _md5
    _hash = _md5(_redump).hexdigest()
    assert _hash == DATA_REGEX_MD5
    os.makedirs(os.path.dirname(DATA_REGEX), exist_ok=True)
    with open(DATA_REGEX, 'wb') as f:
        f.write(_redump)

else:
    with open(DATA_REGEX, 'rb') as f:
        _data = f.read()
    from hashlib import md5 as _md5
    assert _md5(_data).hexdigest() == DATA_REGEX_MD5
    class RE: pass
    _ = pickle.loads(_data)
    for k, r in _.items():
        setattr(RE, k, r)


def generalize_oracle(oracle_text: str, count_i: int):
    if not oracle_text:
        return

    card = oracle_text

    if card[-1] == '.':
        card = card[:-1]

    # Make the text parsable by NLTK
    for k, v in CONTRACTIONS.items():
        if k in card:
            card = card.replace(k, v)

    # These cause issues, so nip it immediately
    for k,v in {
        '"legend rule"': 'LEGEND_RULE',
        '"bands with other"': 'BANDS_WITH_OTHER',
    }.items():
        if k in card:
            card = card.replace(k,v)

    # Remove these specifically because we don't care about them for analysis
    if '[' in card:
        card = card.replace('[', '').replace(']', '')

    if '{CHAOS}' in card:
        card = card.replace('{CHAOS}', 'CHAOS')

    # Remove any sub-actions (IE ~ gives some "Text")
    tokens = word_tokenize(card)
    if '"' in card:
        t = []
        is_sub = False
        for token in tokens:
            if token == '``':
                token = '"'
            if token == "''":
                token = '"'
            if '"' in token:
                if not is_sub:
                    is_sub = True
                elif is_sub:
                    is_sub = False
                    continue
            if not is_sub and token:
                if token in ":,'.":
                    if not t:
                        t.append('')
                    t[-1] += token
                else:
                    t.append(token)
        joined = ' '.join(t)
        # for k,v in CONTRACTIONS.items():
        #     joined = joined.replace(v, k)
        if '{' in joined:
            joined = re.sub(r'\{\s*(.*?)\s*\}', r'{\1}', joined)
        if '} {' in joined:
            joined = joined.replace('} {', '}{')
        if '[' in joined:
            joined = re.sub(r'\[\s*(.*?)\s*\]', r'[\1]', joined)
        card = joined + ' SUB_TEXT'
        tokens = word_tokenize(card)

    # for k,v in CONTRACTIONS.items():
    #     card = card.replace(v,k)

    # Convert out { } items
    for k,v in {
        '{T}': 'TAP',
        '{Q}': 'UNTAP',
        '{E}': 'ENERGY',
        '{TK}': 'TICKET'
    }.items():
        card = card.replace(k,v)

    # Fix spacing issues
    if (match := RE.SPACING.search(card)):
        card = card[:match.start(0)] + ' ' + card[match.start(0)] + ' ' + card[match.end(0):]

    # Convert out costs
    card = RE.COST.sub('MANA', card)

    # Turn upkeep into upkeep step
    if 'upkeep' in card:
        card = card.replace('upkeep steps', 'upkeep')
        card = card.replace('upkeep step', 'upkeep')
        card = card.replace('upkeep', 'upkeep step')

    # Convert out steps / phases
    while (match := RE.STEP_PHASE.search(card)):
        card = card[:match.start(0)] + 'STEP_OR_PHASE' + card[match.end(0):]

    # Convert out PW abilities
    if (match := RE.PW_ABILITY.search(card)):
        card = card[:match.start(1)] + 'PW_COST' + card[match.end(1):]

    # Convert out LEVELs
    if (match := RE.CLASS_LEVEL.search(card)):
        card = card[:match.start(0)] + 'CLASS_LEVEL' + card[match.end(0):]

    # Convert out Roman Numerals
    if (match := RE.ROMANS.search(card)):
        card = card[:match.start(1)] + 'SAGA_LEVEL_S' + card[match.end(1):]

    # Convert out d20 rolls
    if (match := RE.D20.search(card)):
        card = card[:match.start(0)] + 'D20_ROLL' + card[match.end(0):]

    # Convert out P/T mods
    while (match := RE.PT.search(card)):
        card = card[:match.start(0)] + 'PT' + card[match.end(0):]
    while (match := RE.PT_MOD.search(card)):
        card = card[:match.start(0)] + 'PT_MOD' + card[match.end(0):]

    # Convert out named cards
    while (match := RE.NAMED.search(card)):
        card = card[:match.start(0)] + 'CARD_NAME' + card[match.end(0):]

    # Convert out named keywords / abilities
    for replace, regex_patterns in RE.ABILITY_PATTERNS.items():
        for regex_pattern in regex_patterns:
            while (match := regex_pattern.search(card)):
                prefix = match.group(1)
                start_index = match.start(1)
                end_index = match.end(0)

                pieces = [card[:start_index], prefix + replace, card[end_index:]]

                digits_match = RE.ABILITY_DIGIT_MATCH.match(pieces[2])
                if digits_match:
                    pieces[2] = ' ' + pieces[2][digits_match.end():]
                    if pieces[2][:2] in (' .', '  ', ' ,'):
                        pieces[2] = pieces[2][1:]

                card = ''.join(pieces).strip()
                match = regex_pattern.search(card)

    # Convert out choose
    if (match := RE.CHOOSE_ONE.search(card)):
        card = card[:match.start(0)] + 'CHOOSE_ITEM_S' + card[match.end(0):]

    # Convert out implicit abilities
    if (match := RE.IMPLICIT_ABILITY.search(card)):
        card = card[:match.pos] + 'ABILITY_IMPLICIT' + card[match.end(1):]

    # Convert out role tokens
    while (match := RE.SUB_TYPES.search(card)):
        card = card[:match.start(0)] + 'SUB_TYPE' + card[match.end(0):]

    # Convert out sub types
    while (match := RE.SUB_TYPES.search(card)):
        card = card[:match.start(0)] + 'SUB_TYPE' + card[match.end(0):]

    # Convert out card types
    while (match := RE.CARD_TYPES.search(card)):
        card = card[:match.start(0)] + 'CARD_TYPE' + card[match.end(0):]

    # Convert out super types
    while (match := RE.SUPER_TYPES.search(card)):
        card = card[:match.start(0)] + 'SUPER_TYPE' + card[match.end(0):]

    # Convert out counters

    # Get rid of capital letters for start of sentences
    # This is specifically done after implicits but before named cards
    # if not '—' in card:
    #     card = card[0].lower() + card[1:]
    # card = re.sub()

    # Convert out digits
    while (match := RE.BASIC_DIGITS.search(card)):
        card = card[:match.start(0)] + 'DIGIT' + card[match.end(0):]

    # Convert out named numbers (one, two, etc)

    # Fix possesives
    while (match := RE.POSSESSIVE.search(card)):
        card = card[:match.start(0)] + ' POSSESSIVE' + card[match.end(0):]

    # Fix energy tokens
    if (match := RE.ENERGY_TOKEN.search(card)):
        card = card[:match.start(0)] + 'ENERGY' + card[match.end(0):]


    # These are specific rules that we need to convert
    if card in (
        'legend rule',
        'bands with other'
    ):
        card = '_'.join([x.upper() for x in card.split()])

    # Lowercase the first word if necessary
    # This approach is not exhaustive
    # for splitter in ':—|':
    #     pieces = card.split(splitter)
    #     for piece in pieces:
    #         splits = piece.split()
    #         i = 0
    #         while i < len(splits) and len(splits[i]) == 1 and not splits[i].isalnum():
    #             i += 1
    #         first_word = splits[i]
    #         if (len(first_word) == 1 and first_word.isalpha() and first_word == 'A') or not first_word.isupper():
    #             card = card[:card.index(first_word)] + first_word.lower() + card[card.index(first_word) + len(first_word):]

    # Not sure what caused this bug, but this is the easiest fix
    card = card.replace(" '", "'")

    # Lowercase words where necessary
    words = card.split()
    for i, word in enumerate(words):
        if word == 'A' or not word.isupper():
            words[i] = word.lower()
    card = ' '.join(words)

    return card


def main():
    with open(DATA_FILE_ORACLE) as f:
        data = [
            generalize_oracle(text, i)
            for i, oracle_text in enumerate(f.read().split('\n'))
            if oracle_text
            for text in oracle_text.split('. ')
        ]

    # DECIMATE_THE_DECIMAL = True
    # if DECIMATE_THE_DECIMAL:
    #     _ = []
    #     for x in data:
    #         for y in x.split('. '):
    #             _.append(y)
    #     data = _

    SORT_AND_FILTER = True
    if SORT_AND_FILTER:
        _ = []
        for x in data:
            if x not in _:
                _.append(x)
        _.sort()
        data = _

    with open(DATA_FILE_OUT, 'w') as f:
        for x in data:
            f.write(x + '\n')

if __name__ == '__main__':
    main()
