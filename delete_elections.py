import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chemie.chemie.settings'
from django import setup
setup()
from chemie.elections.models import Election, Position, Candidate

Election.objects.all().delete()
Position.objects.all().delete()
Candidate.objects.all().delete()
