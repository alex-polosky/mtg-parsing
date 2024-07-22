from scripts.generalize_oracle_text import generalize_oracle

data = []
for i, x in enumerate([
    # '''{B}{B}{B}, {T}: Destroy target creature. If that creature dies this way, create a black Vampire creature token. Its power is equal to that creature's power and its toughness is equal to that creature's toughness.''',
    # '''{T}: Put target creature card from your graveyard on top of your library. Activate only during your turn, before attackers are declared.''',
    # '{T}: A player of your choice adds {C}.',
    "At the beginning of combat on your turn, equipped creature or a creature you control named Vecna gets +X/+X until end of turn, where X is the number of cards in your hand.",
    'Heroic — Whenever you cast a spell that targets ~, create a 0/1 red Kobold creature token named Kobolds of Kher Keep.'
]):
    data.append(generalize_oracle(x, i))

with open('data/testing.txt', 'w') as f:
    f.write('\n'.join(sorted(data)))
