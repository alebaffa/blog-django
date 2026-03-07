import frontmatter
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from posts.models import Post, Tag

CONTENT_DIR = Path(__file__).resolve().parents[3] / 'content' / 'posts'


class Command(BaseCommand):
    help = 'Sync markdown files from content/posts/ into the database'

    def handle(self, *args, **kwargs):
        if not CONTENT_DIR.exists():
            self.stdout.write(self.style.WARNING(f'Content directory not found: {CONTENT_DIR}'))
            return

        md_files = list(CONTENT_DIR.glob('*.md'))
        if not md_files:
            self.stdout.write(self.style.WARNING('No markdown files found.'))
            return

        created = updated = 0

        for path in md_files:
            post_meta = frontmatter.load(path)
            slug = post_meta.get('slug') or slugify(path.stem)
            title = post_meta.get('title', path.stem)
            body = post_meta.content
            status = post_meta.get('status', 'draft')
            published_at = post_meta.get('published_at')
            excerpt = post_meta.get('excerpt', '')

            import datetime
            if published_at and isinstance(published_at, datetime.date) and not isinstance(published_at, datetime.datetime):
                published_at = timezone.make_aware(datetime.datetime(published_at.year, published_at.month, published_at.day))
            elif published_at and isinstance(published_at, datetime.datetime) and timezone.is_naive(published_at):
                published_at = timezone.make_aware(published_at)

            post, is_new = Post.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'body': body,
                    'excerpt': excerpt,
                    'status': status,
                    'published_at': published_at,
                },
            )

            tag_names = post_meta.get('tags', [])
            if isinstance(tag_names, str):
                tag_names = [t.strip() for t in tag_names.split(',')]

            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
                tags.append(tag)
            post.tags.set(tags)

            if is_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {title}'))
            else:
                updated += 1
                self.stdout.write(f'  Updated: {title}')

        self.stdout.write(self.style.SUCCESS(f'Done. {created} created, {updated} updated.'))
