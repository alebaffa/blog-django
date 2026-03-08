from django.contrib import admin

from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "published_at", "created_at"]
    list_filter = ["status", "tags"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["title", "slug", "status"]}),
        ("Content", {"fields": ["body", "excerpt", "cover_image"]}),
        ("Metadata", {"fields": ["tags", "published_at", "created_at", "updated_at"]}),
    ]
