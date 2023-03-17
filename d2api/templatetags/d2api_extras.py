from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return round(value * arg)

@register.filter(name='percentize')
def percentize(value):
    return round(value * 3.33)
