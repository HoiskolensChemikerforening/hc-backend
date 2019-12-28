from django import template
from django.utils import timezone
from django.views.decorators.cache import cache_page

from chemie.chemie.models import Sponsor

register = template.Library()


@cache_page(60 * 60)
@register.inclusion_tag("chemie/sponsor_list.html")
def show_sponsors():
    sponsors = Sponsor.objects.filter(end_date__gte=timezone.now())
    return {"sponsors": sponsors}
