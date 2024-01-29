from django import forms
import material as M
from .models import Travelletter, Experience, Questions
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseFormSet, BaseModelFormSet
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
        fields = ['question', 'answer']



class SensibleFormset(BaseModelFormSet):
    def total_form_count(self):
        """Returns the total number of forms in this FormSet."""
        if self.data or self.files:
            return self.management_form.cleaned_data['TOTAL_FORMS']
        else:
            if self.initial_form_count() > 0:
                total_forms = self.initial_form_count()
            else:
                total_forms = self.initial_form_count() + self.extra
            if total_forms > self.max_num > 0:
                total_forms = self.max_num
            return total_forms

ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, formset=SensibleFormset)




