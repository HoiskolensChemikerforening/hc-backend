from django import template
from django.utils import timezone
from django.views.decorators.cache import cache_page



register = template.Library()


@cache_page(60 * 60)
@register.inclusion_tag("chemie/sponsor_list.html")
def show_sponsors():
    from chemie.chemie.models import Sponsor
    sponsors = Sponsor.objects.filter(end_date__gte=timezone.now())
    return {"sponsors": sponsors}
