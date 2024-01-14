import os

from django.template.defaulttags import register

from config.settings import BASE_DIR


@register.filter
def get_name_or_email(user, default='Неизвестно'):
    if user:
        return user.username or user.email or default
    return default


@register.filter
def get_item(iterable: dict, key):
    if isinstance(iterable, dict):
        return iterable.get(key)
    elif isinstance(iterable, list):
        return iterable[int(key)]


@register.filter
def list_breaks(string: str):
    return string.split(';')


@register.inclusion_tag(BASE_DIR / 'templates/includes/button_navigation.html', name='btn_nav')
def button_navigation(paginator, page_obj):
    return {'paginator': paginator, 'page_obj': page_obj}


@register.filter
def file_exists(path):
    return os.path.exists(path)
