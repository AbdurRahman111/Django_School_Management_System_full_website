from django import template

register = template.Library()

@register.filter(name='get_value')

def get_value(dict, key):
    return dict.get(key)
