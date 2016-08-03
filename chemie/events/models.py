from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField
#from customprofile.models import Profile
from extended_choices import Choices
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

REGISTRATION_STATUS = Choices(
    ('CONFIRMED',  1, 'Confirmed'),
    ('WAITING', 2, 'Waiting'),
)

class Event(models.Model):
    # Name of the event
    title = models.CharField(max_length=40, verbose_name='Tittel')

    # Name of person creating event
    author = models.ForeignKey(User, related_name="author")

    #  When the event occurs, is created and edited
    date = models.DateTimeField(default=timezone.now, verbose_name="Dato")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Start time for registration
    register_startdate = models.DateTimeField(default=timezone.now, verbose_name="Påmeldingen åpner")

    # Deadline for signing up
    register_deadline = models.DateTimeField(default=timezone.now, verbose_name="Påmeldingsfrist")

    # Deadline for changing your mind
    deregister_deadline = models.DateTimeField(default=timezone.now, verbose_name="Avmeldingsfrist")

    # Location of event
    location = models.TextField(verbose_name="Sted")

    # Describes the event
    description = models.TextField(verbose_name="Beskrivelse", max_length=400)

    # An image from the event or describing the event
    image = ImageField(upload_to='events', verbose_name="Bilde")

    # Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(default=100, verbose_name="Antall plasser")

    # Payment information
    payment_information = models.CharField(verbose_name="Betalingsinformasjon", max_length=400)
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

    def registered_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.CONFIRMED).count()

    def waiting_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.WAITING).count()

    def spare_slots(self):
        return self.sluts - self.registered_users()

    def has_spare_slots(self):
        return self.spare_slots() > 0

    def register_user(self, User):
        if self.spare_slots():
            self.attendees.add(User)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={"event_id":self.id})

    def get_absolute_registration_url(self):
        return reverse('events:register', kwargs={"event_id":self.id})

    @property
    def is_open(self):
        return timezone.now() > self.register_startdate

class RegistrationManager(models.Manager):
    def de_register(self, event, reg_to_be_deleted):
        reg_to_be_deleted.delete()
        waiting = self.filter(event=event, status = REGISTRATION_STATUS.WAITING)
        if waiting:
            lucky_person = waiting.earliest('created').confirm()
            return lucky_person

class Registration(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.WAITING)
    payment_status = models.BooleanField(default=False, verbose_name="Betalt")

    # Optional fields
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    companion = models.CharField(max_length=40, verbose_name="Navn på følge",
                                 help_text="Navn på ekstern person. Ønske om bordkavaler sendes til festkom.",
                                 null=True, blank=True)

    objects = RegistrationManager()

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.user.get_full_name(), self.status)

    def confirm(self):
        self.status = REGISTRATION_STATUS.CONFIRMED

    class Meta:
        unique_together = ('event', 'user',)

