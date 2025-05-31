# app/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def in_groups(user, group_names):
    return user.groups.filter(name__in=group_names.split(',')).exists()
