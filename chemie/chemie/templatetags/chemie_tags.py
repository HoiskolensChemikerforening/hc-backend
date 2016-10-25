from django import template
from chemie.models import Sponsor
from django.utils import timezone
register = template.Library()

@register.inclusion_tag('sponsor/sponsor_list.html')
def show_sponsors():
    sponsors = Sponsor.objects.filter(end_date__gte=timezone.now())
    return {'sponsors': sponsors}