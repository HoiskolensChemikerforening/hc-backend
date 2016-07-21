from django import forms
import material as M
from .models import Event

class RegisterEvent(forms.ModelForm):
    layout = M.Layout(M.Row('title'),
                      M.Row('date'),
                      M.Row('register_startdate', 'register_deadline','deregister_deadline'),
                      M.Row('location'),
                      M.Row('description'),
                      M.Row('sluts'),
                      M.Row('price_member','price_not_member','price_companion'),
                      M.Row('companion','sleepover', 'night_snack','mail_notification'),)


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