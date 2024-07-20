from scripts.generalize_oracle_text import generalize_oracle

for i, x in enumerate([
    # '''{B}{B}{B}, {T}: Destroy target creature. If that creature dies this way, create a black Vampire creature token. Its power is equal to that creature's power and its toughness is equal to that creature's toughness.''',
    # '''{T}: Put target creature card from your graveyard on top of your library. Activate only during your turn, before attackers are declared.''',
    '{T}: A player of your choice adds {C}.',
]):
    generalize_oracle(x, i)
