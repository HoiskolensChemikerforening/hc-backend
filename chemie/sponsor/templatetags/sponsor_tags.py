from django import template
from sponsor.models import Sponsor


register = template.Library()

@register.inclusion_tag('sponsor/sponsor_list.html')

def show_sponsors():
    temp_sponsors = Sponsor.objects.all()
    sponsors = []
    for sponsor in temp_sponsors:
        if not sponsor.is_expired():
            sponsors.append(sponsor)

    return {'sponsors': sponsors}
