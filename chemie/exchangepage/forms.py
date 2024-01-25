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

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question']

class TravelletterForm(forms.ModelForm):
    class Meta:
        model = Travelletter
        fields = ['user', 'country', 'city', 'sun', 'livingExpences', 'availability', 'nature', 'hospitality', 'workLoad']



class ExperienceForm(forms.ModelForm):
    questions_info = QuestionsForm()
    travelletter_info = TravelletterForm()
    class Meta:
        model = Experience
        fields = ['answer']

    def save(self, commit=True):
        questions_instance = self.questions_info.save(commit)
        travelletter_instance = self.travelletter_info.save(commit)
        experience_instance = super().save(commit=False)
        experience_instance.question = questions_instance
        experience_instance.travelletter = travelletter_instance

        if commit:
            experience_instance.save()

        return experience_instance



