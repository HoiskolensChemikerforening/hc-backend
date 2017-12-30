import material as M
from django import forms
from django.core.validators import ValidationError

from customprofile.models import GRADES
from .models import Social, EventRegistration, Bedpres, BedpresRegistration, BaseEvent


class BaseRegisterEventForm(forms.ModelForm):
    allowed_grades = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=GRADES,
        label='Tillatte klassetrinn',
    )

    def clean(self):
        super(BaseRegisterEventForm, self).clean()
        if not self.is_valid():
            return

        event_date, open_date = self.cleaned_data['date'], self.cleaned_data['register_startdate']
        deadline, lock_in_date = self.cleaned_data['register_deadline'], self.cleaned_data['deregister_deadline']

        if event_date < open_date:
            self.add_error(None, ValidationError(
                {'register_startdate': ["Påmeldingen må være før arrangementet begynner"]}))

        if event_date < deadline:
            self.add_error(None, ValidationError(
                {'register_deadline': ["Påmeldingsfristen må være før arrangementet begynner"]}))

        if event_date < lock_in_date:
            self.add_error(None, ValidationError(
                {'deregister_deadline': ["Avmeldingsfristen må være før arrangementet begynner"]}))

        if deadline < open_date:
            self.add_error(None, ValidationError(
                {'register_deadline': ["Påmeldingsfristen må være etter påmeldingen begynner"]}))

    def clean_allowed_grades(self):
        try:
            grades = self.cleaned_data.get('allowed_grades')
            grades = [int(grade) for grade in grades]
            _ = [GRADES.values[int(grade)] for grade in grades]
            return grades
        except (ValueError, KeyError):
            self.add_error(None, ValidationError(
                {'allowed_grades': ["Tillatte klassetrinn er ikke akseptert"]}))

    class Meta:
        abstract = True
        model = BaseEvent
        fields = [
            "title",
            "location",
            "description",
            "image",
            "sluts",
            "allowed_grades",
            "date",
            "register_startdate",
            "register_deadline",
            "deregister_deadline",
            "published"
        ]
        field_classes = {
            'date': forms.SplitDateTimeField,
            'register_startdate': forms.SplitDateTimeField,
            'register_deadline': forms.SplitDateTimeField,
            'deregister_deadline': forms.SplitDateTimeField,
        }


class RegisterEventForm(BaseRegisterEventForm):
    layout = M.Layout(M.Row(M.Column('published','title', )),
                      M.Row(M.Column('date', span_columns=1),
                            M.Column('register_startdate', span_columns=1),
                            M.Column('register_deadline', span_columns=1),
                            M.Column('deregister_deadline', span_columns=1)),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('payment_information'),
                      M.Row(M.Column('image'), M.Column('sluts')),
                      M.Row('price_member', 'price_not_member', 'price_companion'),
                      M.Row('companion', 'sleepover', 'night_snack'),
                      M.Row('allowed_grades')
                      )

    class Meta(BaseRegisterEventForm.Meta):
        model = Social
        fields = BaseRegisterEventForm.Meta.fields.copy()
        fields += [
            "payment_information",
            "price_member",
            "price_not_member",
            "price_companion",
            "companion",
            "sleepover",
            "night_snack",
        ]


class RegisterBedpresForm(BaseRegisterEventForm):
    layout = M.Layout(M.Row(M.Column('published','title', )),
                      M.Row(M.Column('date', span_columns=1),
                            M.Column('register_startdate', span_columns=1),
                            M.Column('register_deadline', span_columns=1),
                            M.Column('deregister_deadline', span_columns=1)),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row(M.Column('image'), M.Column('sluts')),
                      M.Row('allowed_grades'), )

    class Meta(BaseRegisterEventForm.Meta):
        model = Bedpres
        fields = BaseRegisterEventForm.Meta.fields.copy()


class SocialRegisterUserForm(forms.ModelForm):
    class Meta:
        model = EventRegistration

        fields = [
            "sleepover",
            "night_snack",
            "companion",
        ]

    def __init__(self, *args, **kwargs):
        enable_sleepover = kwargs.pop('enable_sleepover', True)
        enable_night_snack = kwargs.pop('enable_night_snack', True)
        enable_companion = kwargs.pop('enable_companion', True)
        super(SocialRegisterUserForm, self).__init__(*args, **kwargs)
        if not enable_sleepover:
            self.fields.pop('sleepover')
        if not enable_night_snack:
            self.fields.pop('night_snack')
        if not enable_companion:
            self.fields.pop('companion')


class BedpresRegisterUserForm(forms.ModelForm):
    class Meta:
        model = BedpresRegistration
        fields = ()


class DeRegisterUserForm(forms.Form):
    really_sure = forms.BooleanField(required=True, label='Er dette ditt endelige svar?')
