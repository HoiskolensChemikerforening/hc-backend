import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chemie.chemie.settings'
from django import setup
setup()
from chemie.elections.models import Election, Position, Candidates

Election.objects.all().delete()
Position.objects.all().delete()
Candidates.objects.all().delete()
