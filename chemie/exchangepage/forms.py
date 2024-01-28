from django import forms
import material as M
from .models import Travelletter, Experience, Questions
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory
class IndexForm(forms.Form):
    OPTIONS = [
        (1, 'Solfaktor'),
        (2, 'Levekostnader'),
        (3, 'Tilgjengelighet'),
        (4, 'Natur'),
        (5, 'Gjestfrihet'),
        (6, 'Arbeidsmengde')
    ]
    Indexfiltering = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS, required=False)

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question']

class TravelletterForm(forms.ModelForm):
    class Meta:
        model = Travelletter
        fields = ['user', 'country', 'city', 'sun', 'livingExpences', 'availability', 'nature', 'hospitality', 'workLoad']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['answer']


QuestionsFormSet = modelformset_factory(Questions, fields=["question"], extra=1)
ExperienceFormSet = modelformset_factory(Experience, fields=["answer"], extra=1)




