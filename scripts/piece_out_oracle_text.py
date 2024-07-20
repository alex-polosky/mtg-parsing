import os

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE_ORACLE = os.path.join(DATA_DIR, 'out', 'oracle_generalized.txt')
DATA_FILE_ABILITY_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_ability.txt')
DATA_FILE_COST_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_cost.txt')
DATA_FILE_ORACLE_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_text.txt')


def main():
    with open(DATA_FILE_ORACLE) as f:
        data = [x for x in f.read().split('\n') if x]

    abilities = []
    costs = []
    oracles = []

    for card in data:
        split = card.split('—')[::-1]
        split = [x.strip() for x in split[0].split(':')[::-1] + split[1:]]
        while len(split) < 3:
            split.append('')
        oracle, cost, ability = split
        if not ability in abilities: abilities.append(ability)
        if not cost in costs: costs.append(cost)
        if not oracle in oracles: oracles.append(oracle)

    abilities.sort()
    costs.sort()
    oracles.sort()

    with open(DATA_FILE_ABILITY_OUT, 'w') as f:
        for x in abilities:
            if not x:
                continue
            f.write(x + '\n')

    with open(DATA_FILE_COST_OUT, 'w') as f:
        for x in costs:
            if not x:
                continue
            f.write(x + '\n')

    with open(DATA_FILE_ORACLE_OUT, 'w') as f:
        for x in oracles:
            if not x:
                continue
            f.write(x + '\n')

if __name__ == '__main__':
    main()
