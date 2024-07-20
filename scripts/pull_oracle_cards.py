import json
import os
from elasticsearch import Elasticsearch

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
DATA_FILE_OUT = os.path.join(DATA_DIR, 'out', 'oracles_text.ndjson')

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
KIBANA_HOST = os.environ.get('KIBANA_HOST')
ELASTIC_INDEX = os.environ.get('ES_INDEX_MTG')


# Define the query with aggregation
query = {
  "size": 0,
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "set_type.keyword": {
              "query": "core"
            }
          }
        },
        {
          "match": {
            "set_type.keyword": {
              "query": "expansion"
            }
          }
        },
        {
          "match": {
            "set_type.keyword": {
              "query": "commander"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "combined_oracle_texts": {
      "scripted_metric": {
        "init_script": "state.texts = []",
        "map_script": """
          if (doc.containsKey('oracle_text.keyword') && doc['oracle_text.keyword'].size() > 0) {
            def type_line = doc.containsKey('card_faces.type_line.keyword') && doc['card_faces.type_line.keyword'].size() > 0 ? [] : [doc['type_line.keyword'].value];
            state.texts.add(['name': doc['name.keyword'].value, 'oracle': doc['oracle_text.keyword'].value, 'card': doc['name.keyword'].value, 'type': type_line[0]]);
          }
          if (doc.containsKey('card_faces.oracle_text.keyword') && doc['card_faces.oracle_text.keyword'].size() > 0) {
            def card_faces_oracle_texts = doc['card_faces.oracle_text.keyword'];
            def card_faces_names = doc['card_faces.name.keyword'];
            def card_faces_type_lines = doc['card_faces.type_line.keyword'];
            if (card_faces_type_lines.size() == 1) {
              card_faces_type_lines = [card_faces_type_lines[0]];
              while (card_faces_type_lines.size() != card_faces_oracle_texts.size()) {
                card_faces_type_lines.add(card_faces_type_lines[0]);
              }
            }
            for (int i = 0; i < card_faces_oracle_texts.length; i++) {
              state.texts.add(['name': doc['name.keyword'].value, 'oracle': card_faces_oracle_texts[i], 'card': card_faces_names[i], 'type': card_faces_type_lines[0]]);
            }
          }
        """,
        "combine_script": "return state.texts",
        "reduce_script": """
          def result = [];
          for (texts in states) {
            result.addAll(texts);
          }
          return states[0];
        """
      }
    }
  }
}


def get_es():
    return Elasticsearch(ELASTIC_HOST)

def main():
    response = get_es().search(index=ELASTIC_INDEX, body=query)

    oracle_texts = response['aggregations']['combined_oracle_texts']['value']

    # Check the oracle texts to see if there are any "malformed" texts
    names = [card['name'] for card in oracle_texts]
    cards = [card['card'] for card in oracle_texts]
    malformed = [
        name
        for name in names
        if ' // ' in name and False in [card in cards for card in name.split(' // ')]
    ]

    os.makedirs(os.path.dirname(DATA_FILE_OUT), exist_ok=True)
    with open(DATA_FILE_OUT, 'w') as f:
        for card in oracle_texts:
            if card['name'] in malformed:
                continue
            f.write(json.dumps(card) + '\n')


if __name__ == '__main__':
    main()
