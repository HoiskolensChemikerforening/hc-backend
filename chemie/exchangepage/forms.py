from django import forms
import material as M
from .models import Travelletter, Experience, Questions, Images
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseModelFormSet
class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question']

class TravelletterForm(forms.ModelForm):
    class Meta:
        model = Travelletter
        fields = ['user', 'country', 'city', 'sun', 'livingExpences', 'availability', 'nature', 'hospitality', 'workLoad', 'destinationInfo']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['question', 'answer']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']

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

class SensibleFormset2(BaseModelFormSet):
    def total_form_count(self):
        """Returns the total number of forms in this FormSet."""
        if self.data or self.files:
            return len(self.files)
        else:
            if self.initial_form_count() > 0:
                total_forms = self.initial_form_count()
            else:
                total_forms = self.initial_form_count() + self.extra
            if total_forms > self.max_num > 0:
                total_forms = self.max_num
            return total_forms


ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, formset=SensibleFormset)
ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=1, formset=SensibleFormset)




