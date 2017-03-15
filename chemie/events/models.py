from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from extended_choices import Choices
from sorl.thumbnail import ImageField
from customprofile.models import GRADES

from .email import send_event_mail

REGISTRATION_STATUS = Choices(
    ('CONFIRMED', 1, 'Confirmed'),
    ('WAITING', 2, 'Waiting'),
)


class Limitation(models.Model):
    grade = models.PositiveSmallIntegerField(choices=GRADES, verbose_name="Klassetrinn")
    slots = models.PositiveSmallIntegerField(default=100, verbose_name="Antall plasser")


class BaseEvent(models.Model):
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
    description = RichTextField(verbose_name='Beskrivelse', config_name='events')


    # An image from the event or describing the event
    image = ImageField(upload_to='events', verbose_name="Bilde")

    # Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(default=100, verbose_name="Antall plasser")

    attendees = models.ManyToManyField(User, through='BaseRegistration')

    limitations = models.ManyToManyField(Limitation, blank=True)

    def __str__(self):
        return self.title

    def registered_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.CONFIRMED, event=self).count()

    def waiting_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.WAITING, event=self).count()

    @property
    def can_signup(self):
        return (timezone.now() >= self.register_startdate) and (timezone.now() <= self.register_deadline)

    @property
    def can_de_register(self):
        return timezone.now() <= self.deregister_deadline

    def percentage_filled(self):
        try:
            return round((self.attendees.all().count() / self.sluts) * 100)
        except ZeroDivisionError:
            return "N/A"

    class Meta:
        abstract = True


class Event(BaseEvent):
    # Payment information
    payment_information = models.TextField(verbose_name="Betalingsinformasjon", max_length=500)
    price_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, medlem")
    price_not_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, ikke-medlem")
    price_companion = models.PositiveSmallIntegerField(default=0, verbose_name="Pris for følge")

    # Boolean fields
    companion = models.BooleanField(default=False, verbose_name="Følge")
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    mail_notification = models.BooleanField(default=False, verbose_name="E-postbekreftelse")

    attendees = models.ManyToManyField(User, through='EventRegistration')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self.bump_waiting()

    def bump_waiting(self):
        if self.waiting_users():
            if self.has_spare_slots:
                attendees = self.attendees.through.objects.filter(status=REGISTRATION_STATUS.WAITING).order_by('id')[:self.spare_slots]
                for attendee in attendees:
                    attendee.confirm()
                    send_event_mail(attendee, self)

    def registered_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.CONFIRMED, event=self).count()

    def waiting_users(self):
        return self.attendees.through.objects.filter(status=REGISTRATION_STATUS.WAITING, event=self).count()

    @property
    def spare_slots(self):
        return self.sluts - self.registered_users()

    @property
    def has_spare_slots(self):
        return self.spare_slots > 0

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={"event_id": self.id})

    def get_absolute_registration_url(self):
        return reverse('events:register', kwargs={"event_id": self.id})

    @property
    def can_signup(self):
        return (timezone.now() >= self.register_startdate) and (timezone.now() <= self.register_deadline)

    @property
    def can_de_register(self):
        return timezone.now() <= self.deregister_deadline

    def registration_has_opened(self):
        return timezone.now() >= self.register_startdate

#class CompanyEvent(BaseEvent):
#    pass


class RegistrationManager(models.Manager):
    def de_register(self, reg_to_be_deleted):
        event = reg_to_be_deleted.event
        reg_to_be_deleted.delete()
        waiting = self.filter(event=event, status=REGISTRATION_STATUS.WAITING)
        if waiting:
            if event.has_spare_slots:
                sorted_waiting = waiting.order_by('created')
                lucky_person = sorted_waiting[0]
                lucky_person.confirm()
                return lucky_person


class BaseRegistration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(BaseEvent)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.WAITING)

    objects = RegistrationManager()

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.user.get_full_name(), self.status)

    def confirm(self):
        self.status = REGISTRATION_STATUS.CONFIRMED
        self.save()

    class Meta:
        abstract = True
        unique_together = ('event', 'user',)


class EventRegistration(BaseRegistration):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    payment_status = models.BooleanField(default=False, verbose_name="Betalt")

    # Optional fields
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    companion = models.CharField(max_length=40, verbose_name="Navn på følge",
                                 help_text="Navn på ekstern person. Ønske om bordkavaler sendes til festkom.",
                                 null=True, blank=True)


class RegistrationMessage(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    message = models.TextField()
    author = models.ForeignKey(User, related_name="event_message")

    # TODO: legge til author
    def __str__(self):
        return '{}, {}: {}'.format(self.event, self.user, self.message)
