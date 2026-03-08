# Django Blog

A personal blog built with Django 6, deployable on Render's free tier.

## Features

- Minimal home page with inline About section
- Post list (title + date only, paginated)
- Posts written in Markdown with YAML frontmatter, synced to the DB on deploy
- Tag filtering
- WaniKani review statistics page (cached, ETag-aware)
- Django admin for content management
- Draft/Published status workflow

## Project structure

```
config/                  Django project config (settings, urls, wsgi)
apps/
  blog/                  Blog app (models, views, admin, templatetags)
    content/posts/       Markdown post files — edit these to write posts
    management/commands/ sync_posts management command
    migrations/
  wanikani/              WaniKani stats app (API service, view)
  templates/             All HTML templates
static/css/              Custom CSS
Makefile                 Dev shortcuts
render.yaml              Render deployment config
requirements.txt         Production dependencies
requirements-dev.txt     Dev dependencies (linters, type checker)
pyproject.toml           Pylint + isort configuration
mypy.ini                 Mypy + django-stubs configuration
```

## Local setup

```bash
cp .env.example .env        # add your SECRET_KEY and WANIKANI_API_TOKEN
make install                # install dev dependencies
make migrate
make createsuperuser
make run                    # http://localhost:8000
```

## Writing posts

Create a Markdown file in `apps/blog/content/posts/`:

```markdown
---
title: My Post Title
tags: python, django
status: published
published_at: 2026-03-07
excerpt: A short summary shown on the list page.
---

Post content here in **Markdown**.
```

Then sync locally with `make sync_posts`, or just push — Render runs it automatically on every deploy.

## Code quality

```bash
make lint        # ruff + isort + black + pylint (check only)
make lint-fix    # auto-fix ruff + isort + black
make mypy        # static type checking
```

## Deploy to Render (free tier)

Render's web service is free, but they no longer offer a free managed PostgreSQL.
Use [Neon](https://neon.tech) for a free PostgreSQL database (no credit card required).

1. Sign up at [neon.tech](https://neon.tech), create a project, copy the connection string
2. Push this repo to GitHub
3. Go to [render.com](https://render.com) → **New → Blueprint** and connect your repo
4. In the Render dashboard set these environment variables:
   - `DATABASE_URL` — your Neon connection string
   - `WANIKANI_API_TOKEN` — your WaniKani personal access token

Render reads `render.yaml` and handles the rest: installing dependencies, collecting static files, running migrations, and syncing posts on each deploy.
