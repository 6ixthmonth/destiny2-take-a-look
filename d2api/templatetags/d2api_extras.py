from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return round(value * arg)
