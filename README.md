# Django Microservices Template

"fun blurb here"

## Setup

`docker compose build`

`docker compose up -d`

`docker compose exec -it _api python manage.py migrate`

`docker compose exec -it _api python manage.py createsuperuser`

## Running commands

### Admin console

Open [the server page](http://localhost:8999/admin/) to view the admin dash!

### Running test suite

`docker compose --profile test up -d && docker compose logs --since 0s -f _api_test`
