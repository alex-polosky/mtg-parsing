import os

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE_ORACLE = os.path.join(DATA_DIR, 'out', 'oracle_generalized.txt')
DATA_FILE_ABILITY_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_ability.txt')
DATA_FILE_COST_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_cost.txt')
DATA_FILE_ORACLE_OUT = os.path.join(DATA_DIR, 'out', 'oracle_gen_text.txt')


def get_datas(data: list[str]):
    abilities = []
    costs = []
    oracles = []

    for card in data:
        split = card.split('—')[::-1]
        split = [x.strip() for x in split[0].split(':')[::-1] + split[1:]]
        while len(split) < 3:
            split.append('')
        oracle, cost, ability = split
        if ability and not ability in abilities: abilities.append(ability)
        if cost and not cost in costs: costs.append(cost)
        if oracle and not oracle in oracles: oracles.append(oracle)

    return (sorted(abilities), sorted(costs), sorted(oracles))


def main():
    with open(DATA_FILE_ORACLE) as f:
        data = [x for x in f.read().split('\n') if x]

    (abilities, costs, oracles) = get_datas(data)

    with open(DATA_FILE_ABILITY_OUT, 'w') as f:
        f.write('\n'.join([x for x in abilities if x]))

    with open(DATA_FILE_COST_OUT, 'w') as f:
        f.write('\n'.join([x for x in costs if x]))

    with open(DATA_FILE_ORACLE_OUT, 'w') as f:
        f.write('\n'.join([x for x in oracles if x]))

if __name__ == '__main__':
    main()
