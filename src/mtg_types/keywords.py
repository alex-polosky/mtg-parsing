import os
import re

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'))

with open(os.path.join(DATA_DIR, 'rules', 'keywords.txt')) as f:
    data = f.read()

keywords = re.findall(r'702\.\d+\. ([A-z ]*)', data)
keywords.sort()
keywords = tuple(keywords)
