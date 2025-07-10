# app/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def in_groups(user, group_names):
    return user.groups.filter(name__in=group_names.split(',')).exists()




@register.filter(name='instIterable')
def is_instance_iterable(value):
    """Check if value is NOT iterable (except strings)"""
    if isinstance(value, str):  # Exclude strings from being considered iterable
        return True
    try:
        iter(value)
        return False  # It's iterable (list/tuple/etc)
    except TypeError:
        return True  # It's not iterable