from django import template

register = template.Library()


@register.filter
def price(value):
    if value:
        return '{} kr'.format(value)
    else:
        return 'Gratis'
