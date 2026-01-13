from django import template

register = template.Library()


@register.filter
def media_filter(path):
    if hasattr(path, 'name') and path.name:
        return f"/media/{path.name}"
    elif path:
        return f"/media/{path}"
    return "#"
