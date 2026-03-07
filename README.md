# Django Blog

A personal blog built with Django 6, deployable on Render's free tier.

## Features

- Post list with pagination (5 per page)
- Post detail with full content
- Tag filtering via sidebar tag cloud
- Cover image support
- About page
- Django admin for content management (Posts + Tags)
- Draft/Published status workflow
- Auto-generated slugs and excerpts

## Project structure

```
blog/           Django project (settings, urls, wsgi)
posts/          Blog app (models, views, urls, admin)
templates/      HTML templates (base, post_list, post_detail, about)
static/css/     Custom CSS (clean, responsive, no external dependencies)
render.yaml     Render deployment config
```

## Run locally

```bash
cp .env.example .env
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Then go to `http://localhost:8000/admin` to write posts.

## Deploy to Render (free tier)

Render's web service is free, but they no longer offer a free managed PostgreSQL.
Use [Neon](https://neon.tech) for a free PostgreSQL database (no credit card required).

1. Sign up at [neon.tech](https://neon.tech), create a project, and copy the connection string
2. Push this repo to GitHub
3. Go to [render.com](https://render.com) → **New → Blueprint** and connect your repo
4. In the Render dashboard, set the `DATABASE_URL` environment variable to your Neon connection string

Render reads `render.yaml` and handles the rest: installing dependencies, collecting static files, and running migrations on each deploy.
