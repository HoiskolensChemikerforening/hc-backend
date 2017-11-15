from datetime import datetime

import material as M
from django import forms
from django.core.validators import ValidationError

from customprofile.models import GRADES
from .models import Social, EventRegistration, Bedpres, BedpresRegistration, BaseEvent


class BaseRegisterEventForm(forms.ModelForm):
    event_date = forms.DateField(required=True, label='Arrangementsdato')
    event_time = forms.TimeField(required=True, initial='12:00', label='Arrangementstid')
    registration_start_date = forms.DateField(required=True, label='Åpningsdato')
    registration_start_time = forms.TimeField(required=True, initial='12:00', label='Åpningstid')
    register_deadline_date = forms.DateField(required=True, label='Påmeldingsfristdato')
    register_deadline_time = forms.TimeField(required=True, initial='12:00', label='Påmeldingsfristtidspunkt')
    deregister_deadline_date = forms.DateField(required=True, label='Avmeldingsdato')
    deregister_deadline_time = forms.TimeField(required=True, initial='12:00', label='Avmeldingstidspunkt')
    allowed_grades = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=GRADES,
        )

    def clean(self):
        super(BaseRegisterEventForm, self).clean()
        if not self.is_valid():
            return

        event_date = datetime.combine(self.cleaned_data.get('event_date'), self.cleaned_data.get('event_time'))
        registration_date = datetime.combine(self.cleaned_data.get('registration_start_date'),
                                             self.cleaned_data.get('registration_start_time'))
        registration_deadline = datetime.combine(self.cleaned_data.get('register_deadline_date'),
                                                 self.cleaned_data.get('register_deadline_time'))
        deregister_deadline = datetime.combine(self.cleaned_data.get('deregister_deadline_date'),
                                               self.cleaned_data.get('deregister_deadline_time'))

        if event_date < registration_date:
            self.add_error(None, ValidationError(
                {'registration_start_date': ["Påmeldingen må være før arrangementet begynner"]}))

        if event_date < registration_deadline:
            self.add_error(None, ValidationError(
                {'register_deadline_date': ["Påmeldingsfristen må være før arrangementet begynner"]}))

        if event_date < deregister_deadline:
            self.add_error(None, ValidationError(
                {'deregister_deadline_date': ["Avmeldingsfristen må være før arrangementet begynner"]}))

        if registration_deadline < registration_date:
            self.add_error(None, ValidationError(
                {'register_deadline_date': ["Påmeldingsfristen må være etter påmeldingen begynner"]}))

        self.cleaned_data['date'] = event_date
        self.cleaned_data['register_startdate'] = registration_date
        self.cleaned_data['register_deadline'] = registration_deadline
        self.cleaned_data['deregister_deadline'] = deregister_deadline
        self.instance.date = event_date
        self.instance.register_startdate = registration_date
        self.instance.register_deadline = registration_deadline
        self.instance.deregister_deadline = deregister_deadline

    def clean_allowed_grades(self):
        try:
            grades = self.cleaned_data.get('allowed_grades')
            grades = [int(grade) for grade in grades]
            [GRADES.values[int(grade)] for grade in grades]
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
        ]


class RegisterEventForm(BaseRegisterEventForm):
    '''
    layout = M.Layout(M.Row('title'),
                      M.Row(M.Column('event_date', 'event_time', span_columns=1),
                            M.Column('registration_start_date', 'registration_start_time', span_columns=1),
                            M.Column('register_deadline_date', 'register_deadline_time', span_columns=1),
                            M.Column('deregister_deadline_date', 'deregister_deadline_time', span_columns=1)),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('image'),
                      M.Row('payment_information'),
                      M.Row('sluts'),
                      M.Row('price_member', 'price_not_member', 'price_companion'),
                      M.Row('companion', 'sleepover', 'night_snack'), )

    event_date = forms.DateField(required=True, label='Arrangementsdato')
    event_time = forms.TimeField(required=True, initial='12:00', label='Arrangementstid')
    registration_start_date = forms.DateField(required=True, label='Åpningsdato')
    registration_start_time = forms.TimeField(required=True, initial='12:00', label='Åpningstid')
    register_deadline_date = forms.DateField(required=True, label='Påmeldingsfristdato')
    register_deadline_time = forms.TimeField(required=True, initial='12:00', label='Påmeldingsfristtidspunkt')
    deregister_deadline_date = forms.DateField(required=True, label='Avmeldingsdato')
    deregister_deadline_time = forms.TimeField(required=True, initial='12:00', label='Avmeldingstidspunkt')

    def clean(self):
        super(RegisterEventForm, self).clean()
        if not self.is_valid():
            return

        event_date = datetime.combine(self.cleaned_data.get('event_date'), self.cleaned_data.get('event_time'))
        registration_date = datetime.combine(self.cleaned_data.get('registration_start_date'),
                                             self.cleaned_data.get('registration_start_time'))
        registration_deadline = datetime.combine(self.cleaned_data.get('register_deadline_date'),
                                                 self.cleaned_data.get('register_deadline_time'))
        deregister_deadline = datetime.combine(self.cleaned_data.get('deregister_deadline_date'),
                                               self.cleaned_data.get('deregister_deadline_time'))

        if event_date < registration_date:
            self.add_error(None, ValidationError(
                {'registration_start_date': ["Påmeldingen må være før arrangementet begynner"]}))

        if event_date < registration_deadline:
            self.add_error(None, ValidationError(
                {'register_deadline_date': ["Påmeldingsfristen må være før arrangementet begynner"]}))

        if event_date < deregister_deadline:
            self.add_error(None, ValidationError(
                {'deregister_deadline_date': ["Avmeldingsfristen må være før arrangementet begynner"]}))

        if registration_deadline < registration_date:
            self.add_error(None, ValidationError(
                {'register_deadline_date': ["Påmeldingsfristen må være etter påmeldingen begynner"]}))

        self.cleaned_data['date'] = event_date
        self.cleaned_data['register_startdate'] = registration_date
        self.cleaned_data['register_deadline'] = registration_deadline
        self.cleaned_data['deregister_deadline'] = deregister_deadline
        self.instance.date = event_date
        self.instance.register_startdate = registration_date
        self.instance.register_deadline = registration_deadline
        self.instance.deregister_deadline = deregister_deadline
    '''
    layout = M.Layout(M.Row('title'),
                      M.Row(M.Column('event_date', 'event_time', span_columns=1),
                            M.Column('registration_start_date', 'registration_start_time', span_columns=1),
                            M.Column('register_deadline_date', 'register_deadline_time', span_columns=1),
                            M.Column('deregister_deadline_date', 'deregister_deadline_time', span_columns=1)),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('image'),
                      M.Row('sluts'),
                      M.Row('payment_information'),
                      M.Row('price_member', 'price_not_member', 'price_companion'),
                      M.Row('companion', 'sleepover', 'night_snack'), )

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
    layout = M.Layout(M.Row('title'),
                      M.Row(M.Column('event_date', 'event_time', span_columns=1),
                            M.Column('registration_start_date', 'registration_start_time', span_columns=1),
                            M.Column('register_deadline_date', 'register_deadline_time', span_columns=1),
                            M.Column('deregister_deadline_date', 'deregister_deadline_time', span_columns=1)),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('image'),
                      M.Row('sluts'),
                      M.Row('allowed_grades'),
                      )

    class Meta:
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
