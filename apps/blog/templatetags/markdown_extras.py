import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(value):
    extensions = ["fenced_code", "codehilite", "tables", "toc"]
    return mark_safe(md.markdown(value, extensions=extensions))
