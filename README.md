# h4x0r-website

This repo contains the source of our pawsome h4x0r website!

## Installation

Copy the `.env.example` file and customize your `.env` file (you can use [this service](https://djecrety.ir/) for the Django Secret Key):

```
$ cp .env.example .env
```

Build the services and run them:

```
$ docker compose up -d --build
```

Then launch the following commands to initialize the database and to collect the static assets (CSS, JS...):

```
$ docker compose exec web python manage.py migrate --noinput
$ docker compose exec web python manage.py collectstatic --noinput
```

