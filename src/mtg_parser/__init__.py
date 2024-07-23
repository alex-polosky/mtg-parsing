import re
from types import FrameType
from nltk.tokenize import word_tokenize
from utils.scryfall_card import ScryfallCard

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

RE_COMMENTS = re.compile(r' {0,1}\([^)]*\)')

def get_sub_actions(text: str, is_inner=False):
    if is_inner:
        action_string = '"'
        subaction_string = "'"
    else:
        action_string = "'"
        subaction_string = '"'

    subs = []
    each = text
    for k,v in CONTRACTIONS.items():
        each = each.replace(k,v)
    tokens = word_tokenize(each)
    sub = []
    is_sub = False
    for token in tokens:
        if token == '``':
            token = '"'
        if token == "''":
            token = '"'
        if action_string in token:
            if not is_sub:
                is_sub = True
                token = token[1:]
            elif is_sub:
                is_sub = False
                token = token[:-1]
                if token:
                    if token in f":,.{subaction_string}".split():
                        if not sub:
                            sub.append('')
                        sub[-1] += token
                    else:
                        sub.append(token)
                joined = ' '.join(sub)
                # for k,v in CONTRACTIONS.items():
                #     joined = joined.replace(v, k)
                if '{' in joined:
                    joined = re.sub(r'\{\s*(.*?)\s*\}', r'{\1}', joined)
                if '} {' in joined:
                    joined = joined.replace('} {', '}{')
                if '[' in joined:
                    joined = re.sub(r'\[\s*(.*?)\s*\]', r'[\1]', joined)
                subs.append(joined)
                sub = []
        if is_sub and token:
            if token in f":,.{subaction_string}":
                if not sub:
                    sub.append('')
                sub[-1] += token
            else:
                sub.append(token)

    # Fix typos
    for i, sub in enumerate(subs):
        if "have' " in sub:
            subs[i] = sub.replace("have' ", "have '")

    return [each] + subs

def pre_massage(card: ScryfallCard, oracle_text: str):
    # Get rid of comments
    text = RE_COMMENTS.sub('', oracle_text)

    # Make card self referential
    for i, face in enumerate(card.card_faces or []):
        text = text.replace(face.name, f'~{i}')
    text = text.replace(card.name, '~')

    return text

def parse_text(text: str):
    text = text.strip()

    # Are there possibilities where the first letter should be capitalized?
    text = text[0].lower() + text[1:]

    return {
        'to_parse': text
    }

def split_text(text: str):
    return [
        [sentence[:-1] if sentence.endswith('.') else sentence for sentence in line.split('. ')]
        for line in text.split('\n')
    ]

def split_effect(text: str):
    split = text.split('—')[::-1]
    if len(split) == 1:
        split.append('')
    oracle_and_cost, ability = split

    split = oracle_and_cost.split(':')[::-1]
    if len(split) == 1:
        split.append('')
    oracle, cost = split

    return oracle, cost, ability

def parse_sentences(sentences: list[str], is_inner=True):
    if is_inner:
        action_string = '"'
        subaction_string = "'"
    else:
        action_string = "'"
        subaction_string = '"'

    parsed = {
        'ability': None,
        'cost': None,
        'effect': [],
        'subactions': []
    }

    for j, sentence in enumerate(sentences):
        subactions = get_sub_actions(sentence, is_inner)
        sentences[j] = subactions[0]
        for subaction in subactions[1:]:
            sentences[j] = sentences[j].replace(f'{action_string}{subaction}{action_string}', f'SUBACTION_{len(parsed["subactions"])}')
            parsed['subactions'].append(parse_sentences(split_text(subaction)[0], not is_inner))

    oracle, cost, ability = split_effect(sentences[0])

    if ability:
        parsed['ability'] = parse_text(ability)

    if cost:
        parsed['cost'] = parse_text(cost)

    parsed['effect'].append(parse_text(oracle))

    for sentence in sentences[1:]:
        parsed['effect'].append(parse_text(sentence))

    return parsed

def oracle_parser(card: ScryfallCard, face_i: int = 0):
    if face_i:
        oracle_text = card.card_faces[face_i - 1].oracle_text
    else:
        oracle_text = card.oracle_text

    if not oracle_text:
        return {}

    text = pre_massage(card, oracle_text)

    lines = split_text(text)

    results = []

    for sentences in lines:
        parsed = parse_sentences(sentences)
        results.append(parsed)

    return results

def add_ex(frame: FrameType, depth: int):
    return {
        f'code{depth}': f'{frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno}',
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

def create_parsed_obj(card: ScryfallCard):
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
        return objs
    else:
        parsed, is_exception = parse_or_err(card)
        obj['parsed' if not is_exception else 'except'] = parsed
        return [obj]
