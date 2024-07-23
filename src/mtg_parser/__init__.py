import re
from nltk.tokenize import word_tokenize
from .scryfall_card import ScryfallCard

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

def get_sub_actions(text, is_inner=False):
    if is_inner:
        subaction_string = '"'
        action_string = "'"
    else:
        subaction_string = "'"
        action_string = '"'

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
        if subaction_string in token:
            if not is_sub:
                is_sub = True
                token = token[1:]
            elif is_sub:
                is_sub = False
                token = token[:-1]
                if token:
                    if token in f":,.{action_string}".split():
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
            if token in f":,.{action_string}":
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

def pre_massage(oracle_text):
    # Get rid of comments
    text = RE_COMMENTS.sub('', oracle_text)
    return text

def parse_text(text):
    return {
        'to_parse': text
    }

def split_text(text):
    return [
        [sentence[:-1] if sentence.endswith('.') else sentence for sentence in line.split('. ')]
        for line in text.split('\n')
    ]

def parse_sentences(sentences, is_inner=True):
    if is_inner:
        subaction_string = '"'
        action_string = "'"
    else:
        subaction_string = "'"
        action_string = '"'

    parsed = {
        'ability': None,
        'cost': None,
        'effect': [],
        'subactions': []
    }

    for j, sentence in enumerate(sentences):
        actions = get_sub_actions(sentence, is_inner)
        sentences[j] = actions[0]
        for action in actions[1:]:
            sentences[j] = sentences[j].replace(f'{subaction_string}{action}{subaction_string}', f'SUBACTION_{len(parsed["subactions"])}')
            parsed['subactions'].append(parse_sentences(split_text(action)[0], not is_inner))

    prime = sentences[0]

    split = prime.split('—')[::-1]
    split = [x.strip() for x in split[0].split(':')[::-1] + split[1:]]
    while len(split) < 3:
        split.append('')

    oracle, cost, ability = split

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

    text = pre_massage(oracle_text)

    lines = split_text(text)

    results = []

    for sentences in lines:
        parsed = parse_sentences(sentences)
        results.append(parsed)

    return results
