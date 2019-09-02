from django import template
from chemie.shop.models import Item
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def get_item_pk_from_name(name):
    item = Item.objects.get(name=name)
    return item.pk
