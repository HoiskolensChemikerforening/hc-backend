from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_NTNU(email):
    if not email.endswith(('@stud.ntnu.no', '@ntnu.no', '@ntnu.edu')):
        raise ValidationError(
            _('%(Email)s er ikke en NTNU epost'), params={'Email': email},
        )
