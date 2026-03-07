---
title: Hello World
tags: general
status: published
published_at: 2026-03-07
excerpt: My first post, written in Markdown and synced to the database automatically.
---

Welcome to my blog! This post was written as a plain Markdown file and synced into the database automatically.

## How this works

Posts live in `content/posts/` as `.md` files with a YAML frontmatter block at the top:

```markdown
---
title: My Post Title
tags: python, django
status: published
published_at: 2026-03-07
---

Post content here...
```

When you push to GitHub, Render runs `sync_posts` during the build and your post goes live.

## Writing locally

```bash
# Preview the sync without deploying
.venv/bin/python manage.py sync_posts
.venv/bin/python manage.py runserver
```
