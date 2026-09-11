from django import template

register = template.Library()


@register.filter
def split(value, sep=","):
    return str(value).split(sep)


@register.filter
def index(sequence, i):
    try:
        return sequence[int(i)]
    except (IndexError, TypeError, ValueError):
        return ""
