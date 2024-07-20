import dataclasses
import json
import os
from elasticsearch import Elasticsearch, helpers

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE = os.path.join(DATA_DIR, 'scryfall', 'oracle-cards.json')

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
KIBANA_HOST = os.environ.get('KIBANA_HOST')
ELASTIC_INDEX = os.environ.get('ES_INDEX_MTG')

ELASTIC_CHUNK_SIZE = 100


def create_index(client: Elasticsearch, index: str):
    if not client.indices.exists(index=index):
        client.indices.create(index=index)


class JsonEncoder(json.JSONEncoder):
    """custom json encoder to convert sets to supported list-type"""
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)


def main():
    client = Elasticsearch(ELASTIC_HOST)
    create_index(client, ELASTIC_INDEX)
    with open(DATA_FILE) as f:
        if DATA_FILE.endswith('.ndjson'):
            data = f.read().split('\n')
            data = [json.loads(x) for x in data if x]
        elif DATA_FILE.endswith('.json'):
            data = json.loads(f.read())
    for i in range(0, len(data), ELASTIC_CHUNK_SIZE):
        wr = data[i:i + ELASTIC_CHUNK_SIZE]
        helpers.bulk(client, wr, index=ELASTIC_INDEX)


if __name__ == '__main__':
    main()
