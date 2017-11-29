from django import template

register = template.Library()

@register.filter
def getitem(dictionary, key):
    if dictionary:
        return dictionary.get(str(key))
    return ''
