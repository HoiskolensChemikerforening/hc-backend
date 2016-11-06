from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_http(link):
    if 'http://' not in link and 'https://' not in link:
        raise ValidationError(
            _('%(Link)s er ikke en gyldig URL. Vennligst legg til "http://" eller "https://".'), params={'Link': link},
        )
