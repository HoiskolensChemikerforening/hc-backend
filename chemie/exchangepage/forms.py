from django import forms
from .models import Travelletter, Experience, Questions, Images
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseModelFormSet


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ["question"]


class TravelletterForm(forms.ModelForm):
    class Meta:
        model = Travelletter
        fields = [
            "user",
            "semester",
            "country",
            "city",
            "sun",
            "livingExpences",
            "availability",
            "nature",
            "hospitality",
            "workLoad",
            "destinationInfo",
        ]
        widgets = {
            "semester": forms.TextInput(
                {
                    "placeholder": " Ett semester ('H13'), To semester ('H13/V14')"
                }
            )
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["question", "answer"]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["image"]


class SensibleFormset(BaseModelFormSet):  # Modifikasjon til imageformset
    def total_form_count(self):
        """Returns the total number of forms in this FormSet."""
        if self.data or self.files:
            return self.management_form.cleaned_data["TOTAL_FORMS"]
        else:
            if self.initial_form_count() > 0:
                total_forms = self.initial_form_count()
            else:
                total_forms = self.initial_form_count() + self.extra
            if total_forms > self.max_num > 0:
                total_forms = self.max_num
            return total_forms


ImageFormSet = modelformset_factory(
    Images, form=ImageForm, extra=1, formset=SensibleFormset
)
