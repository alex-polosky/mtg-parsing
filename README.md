# Magic the Gathering - Analysing, Parsing (... and eventually simulation)

"fun blurb here"

## Order of scripts

1. fetch_scryfall
1. ingest_es
1. pull_oracle_cards
1. extract_oracle_text
1. generalize_oracle_text
1. piece_out_oracle_text

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
