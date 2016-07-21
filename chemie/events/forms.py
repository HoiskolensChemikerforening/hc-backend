from django import forms

from .models import Event

class RegisterEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "date",
            "register_startdate",
            "register_deadline",
            "deregister_deadline",
            "location",
            "description",
            #"image",
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