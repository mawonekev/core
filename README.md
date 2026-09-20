# Xenohuru API

REST API for Tanzania tourism. Built with Django.


---

## What is this?

Xenohuru is an open platform for Tanzania tourism data — attractions, regions, weather, tour operators and more. The name comes from "xenos" (explorer in Greek) + "huru" (free in Swahili).

This is the backend API. There's a separate frontend repo.

---

## Stack

- Django 4.2 + Django REST Framework
- PostgreSQL
- JWT auth (djangorestframework-simplejwt)
- Cloudinary for media
- Open-Meteo for weather (free, no API key needed)

---

## Getting started

### Requirements
- Python 3.10+
- PostgreSQL (or SQLite for quick testing)

### Setup

```bash
git clone https://github.com/Xenohuru/core.git
cd core


python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# edit .env with your values

python manage.py migrate
python manage.py runserver
```

API will be at `http://localhost:8000/api/v1/`  
Swagger docs at `http://localhost:8000/api/docs/`  
Admin at `http://localhost:8000/admin/`

### Or with Docker

```bash
cp .env.example .env
# edit .env with your values

docker compose up --build
```

This builds the app image, starts Postgres, runs migrations, and serves
the app on `http://localhost:8000/`. Static files and app logs persist in
named Docker volumes (`docker compose logs web` for live output).

---

## Environment variables

See `.env.example`. Key ones:

```
SECRET_KEY=
DEBUG=True
DB_NAME=, DB_USER=, DB_PASSWORD=, DB_HOST=, DB_PORT=
CLOUDINARY_CLOUD_NAME=, CLOUDINARY_API_KEY=, CLOUDINARY_API_SECRET=
EMAIL_HOST_USER=, EMAIL_HOST_PASSWORD=
FRONTEND_URL=
```

---

## Main endpoints

```
GET  /api/v1/attractions/          list attractions
GET  /api/v1/attractions/<slug>/   attraction detail
GET  /api/v1/regions/              list regions
GET  /api/v1/operators/            tour operators
GET  /api/v1/weather/current/      current weather (pass lat/lng or slug)
POST /api/v1/auth/register/        create account
POST /api/v1/auth/login/           get JWT token
POST /api/v1/feedback/submit/      contact / feedback form
POST /api/v1/feedback/attractions/<slug>/reviews/   submit a review
```

Full endpoint list in the Swagger docs.

---

## Tests & CI

```bash
pip install -r requirements-dev.txt
ruff check .
python manage.py test
```

Jenkins (`Jenkinsfile`) lints, builds the Docker image, and runs migrations
and the test suite against it on every push; `main` deploys automatically
once tests pass, via `docker compose up -d --build` on the production host.

---

## Load sample data

```bash
python manage.py loaddata initial_regions
python manage.py loaddata initial_attractions
```

---

## Contributing

Fork the repo, make your changes on a new branch, open a PR. See [CONTRIBUTING.md](docs/CONTRIBUTORS.md) for more details.

---

## License

Xenohuru API is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License v3.0 as published by
the Free Software Foundation. See [LICENSE](LICENSE) for the full text.

Built in Tanzania 🇹🇿
