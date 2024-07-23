# Magic the Gathering - Analysing, Parsing (... and eventually simulation)

"fun blurb here"

## Order of scripts

### Required before running -anything-

1. fetch_scryfall
1. convert_scryfall_objs
1. get_cards_per_set

### For analysis

1. ingest_es
1. pull_oracle_cards
1. extract_oracle_text
1. generalize_oracle_text
1. piece_out_oracle_text

### For parsing

1. parse_per_set SET_CODE

## Setup

`docker compose build`

`docker compose up -d`

<!-- `docker compose exec -it _api python manage.py migrate`

`docker compose exec -it _api python manage.py createsuperuser` -->

## Running commands

### Admin console

Open [the server page](http://localhost:8999/admin/) to view the admin dash!

### Running test suite

<!-- `docker compose --profile test up -d && docker compose logs --since 0s -f _api_test` -->
