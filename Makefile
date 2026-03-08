PYTHON = .venv/bin/python
MANAGE = $(PYTHON) manage.py
LINT_PATHS = ./apps ./config

# ── Dev server ────────────────────────────────────────────────────────────────

run:
	$(MANAGE) runserver

# ── Django management ─────────────────────────────────────────────────────────

sync_posts:
	$(MANAGE) sync_posts

createsuperuser:
	$(MANAGE) createsuperuser

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

shell:
	$(MANAGE) shell

# ── Code quality ──────────────────────────────────────────────────────────────

lint:
	$(PYTHON) -m ruff check $(LINT_PATHS)
	$(PYTHON) -m isort --check --diff $(LINT_PATHS)
	$(PYTHON) -m black --check --diff $(LINT_PATHS)
	$(PYTHON) -m pylint $(LINT_PATHS)

lint-fix:
	$(PYTHON) -m ruff check --fix-only $(LINT_PATHS)
	$(PYTHON) -m isort $(LINT_PATHS)
	$(PYTHON) -m black $(LINT_PATHS)

mypy:
	$(PYTHON) -m mypy $(LINT_PATHS)

# ── Setup ─────────────────────────────────────────────────────────────────────

install:
	uv pip install --python $(PYTHON) -r requirements-dev.txt
