from django.db import models
from datetime import datetime
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from extended_choices import Choices

REGISTRATION_STATUS = Choices(
    ('CONFIRMED',  1, 'Confirmed'),
    ('WAITING', 2, 'Waiting'),
)

class Event(models.Model):
    # Name of the event
    title = models.CharField(max_length=40)

    #Name of person creating event
    author = models.ForeignKey(User, related_name="author")

    # When the event occurs, is created and edited
    date = models.DateTimeField(default=datetime.now(), verbose_name="Dato")
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)

    # Start time for registration
    register_startdate = models.DateField(default=datetime.now(), verbose_name="Påmeldingen åpner")

    # Deadline for signing up
    register_deadline = models.DateField(default=datetime.now(), verbose_name="Påmeldingsfrist")

    # Deadline for changing your mind
    deregister_deadline = models.DateField(default=datetime.now(), verbose_name="Avmeldingsfrist")

    # Location of event
    location = models.TextField(verbose_name="Sted")

    # Describes the event
    description = models.TextField(verbose_name="Beskrivelse")

    # An image from the event or describing the event
    image = ImageField(upload_to='events', verbose_name="Bilde")

    # Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(default=100, verbose_name="Antall plasser")

    # Payment information
    payment_information = models.TextField(verbose_name="Betalingsinformasjon")
    price_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, medlem")
    price_not_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, ikke-medlem")
    price_companion = models.PositiveSmallIntegerField(default=0, verbose_name="Pris for følge")

    # Boolean fields
    companion = models.BooleanField(default=False, verbose_name="Følge")
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    mail_notification = models.BooleanField(default=False, verbose_name="Epostbekreftelse")

    attendees = models.ManyToManyField(User, through='Registration')

    def __str__(self):
        return self.title

    def spare_slots(self):
        attendee_count = self.attendees.filter(status=REGISTRATION_STATUS.CONFIRMED).count()
        return (self.sluts - attendee_count)

    def register_user(self, User):
        if self.spare_slots():
            self.attendees.add(User)


class Registration(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    created = models.DateField(auto_now=False, auto_now_add=True)
    status = models.IntegerField(choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.WAITING)