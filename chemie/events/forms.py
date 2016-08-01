from django import forms
import material as M
from .models import Event, Registration
from django.utils.dateparse import parse_time
from datetime import datetime, date
from django.core.validators import ValidationError

class RegisterEventForm(forms.ModelForm):
    layout = M.Layout(M.Row('title'),
                      M.Row(M.Column('event_date','event_time', span_columns=1),
                            M.Column('registration_start_date','registration_start_time', span_columns=1),
                            M.Column('register_deadline_date','register_deadline_time', span_columns=1),
                            M.Column('deregister_deadline_date','deregister_deadline_time', span_columns=1)),
                      #M.Row('event_date','event_time'),
                      #M.Row('register_startdate', 'register_deadline','deregister_deadline'),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('image'),
                      M.Row('payment_information'),
                      M.Row('sluts'),
                      M.Row('price_member','price_not_member','price_companion'),
                      M.Row('companion','sleepover', 'night_snack','mail_notification'),)

    event_date = forms.DateField(initial=str(date.today()))
    event_time = forms.TimeField(initial='12:00')
    registration_start_date = forms.DateField(initial=str(date.today()))
    registration_start_time = forms.TimeField(initial='12:00')
    register_deadline_date = forms.DateField(initial=str(date.today()))
    register_deadline_time = forms.TimeField(initial='12:00')
    deregister_deadline_date = forms.DateField(initial=str(date.today()))
    deregister_deadline_time = forms.TimeField(initial='12:00')


    def clean(self):
        super(RegisterEventForm, self).clean()
        event_date = datetime.combine(self.cleaned_data.get('event_date'), self.cleaned_data.get('event_time'))
        registration_date = datetime.combine(self.cleaned_data.get('registration_start_date'), self.cleaned_data.get('registration_start_time'))
        registration_deadline = datetime.combine(self.cleaned_data.get('register_deadline_date'), self.cleaned_data.get('register_deadline_time'))
        deregister_deadline = datetime.combine(self.cleaned_data.get('deregister_deadline_date'), self.cleaned_data.get('deregister_deadline_time'))

        if not event_date:
            raise ValidationError({'event_date':["Feltet er påkrevet."]})

        if not registration_date:
            raise ValidationError({'registration_start_date':["Feltet er påkrevet."]})

        if not registration_deadline:
            raise ValidationError({'register_deadline_date':["Feltet er påkrevet."]})

        if not deregister_deadline:
            raise ValidationError({'deregister_deadline_date':["Feltet er påkrevet."]})


        if event_date < registration_date:
            raise ValidationError({'registration_date':["Påmeldingen må være før arrangementet begynner"]})

        if event_date < registration_deadline:
            raise ValidationError({'registration_start_date':["Påmeldingsfristen må være før arrangementet begynner"]})

        if event_date < deregister_deadline:
            raise ValidationError({'deregister_deadline_date':["Avmeldingsfristen må være før arrangementet begynner"]})

        if registration_deadline < registration_date:
            raise ValidationError({'register_deadline_date':["Påmeldingsfristen må være etter påmeldingen begynner"]})

        if deregister_deadline < registration_date:
            raise ValidationError({'deregister_deadline_date':["Avmeldingsfristen må være etter påmeldingen begynner"]})

        self.cleaned_data['date'] = event_date
        self.cleaned_data['register_startdate'] = registration_date
        self.cleaned_data['register_deadline'] = registration_deadline
        self.cleaned_data['deregister_deadline'] = deregister_deadline




    class Meta:
        model = Event
        fields = [
            "title",
            #"date",
            #"register_startdate",
            #"register_deadline",
            #"deregister_deadline",
            "location",
            "description",
            "image",
            "sluts",
            "payment_information",
            "price_member",
            "price_not_member",
            "price_companion",
            "companion",
            "sleepover",
            "night_snack",
            "mail_notification",
        ]



class RegisterUserForm(forms.ModelForm):
    layout = M.Layout(M.Row('sleepover','night_snack'),
                      M.Row('companion'))

    class Meta:
        model = Registration

        fields = [
            "sleepover",
            "night_snack",
            "companion",
        ]