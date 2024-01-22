from django import forms
import material as M
from .models import Travelletter, Experience, Questions
from chemie.customprofile.models import Profile
from django.forms import inlineformset_factory
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
class createTravelletterForm(forms.ModelForm):

    layout = M.Layout(
        M.Row("user"),
        M.Row("country", "city"),
        M.Row("sun", "livingExpences", "availability"),
        M.Row("nature", "hospitality", "workLoad"),
    )

    class Meta:
        model = Travelletter
        fields = [
            "user",
            "country",
            "city",
            "sun",
            "livingExpences",
            "availability",
            "nature",
            "hospitality",
            "workLoad",
        ]






