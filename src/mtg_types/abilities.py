import os
import re

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'))

with open(os.path.join(DATA_DIR, 'rules', 'abilities.txt')) as f:
    data = f.read()

abilities = re.findall(r'701\.\d+\. ([A-z ]*)', data)
__remove = []
abilities.sort()
for index in range(len(abilities)):
    ability = abilities[index]
    if 'and' in ability:
        __remove.append(ability)
        for each in ability.split(' and '):
            abilities.append(each)
for each in __remove:
    abilities.remove(each)
abilities.append('Landfall')
abilities = tuple(abilities)
