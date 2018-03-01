from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db import models
from django.utils import timezone
from extended_choices import Choices
from sorl.thumbnail import ImageField

from chemie.customprofile.models import GRADES
from .email import send_event_mail

REGISTRATION_STATUS = Choices(
    ('CONFIRMED', 1, 'Confirmed'),
    ('WAITING', 2, 'Waiting'),
    ('INTERESTED', 3, 'Interested')
)

ARRIVAL_STATUS = Choices(
    ('NONE',1, 'Ikke satt'),
    ('PRESENT', 2, 'Møtt'),
    ('TRUANT', 3, 'Ikke møtt'),
)


class BaseEvent(models.Model):
    # Name of the event
    title = models.CharField(max_length=40, verbose_name='Tittel')

    # Name of person creating event
    author = models.ForeignKey(User, related_name="baseevent", on_delete=models.CASCADE)

    #  When the event occurs, is created and edited
    date = models.DateTimeField(verbose_name="Dato")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Start time for registration
    register_startdate = models.DateTimeField(verbose_name="Påmeldingen åpner")

    # Deadline for signing up
    register_deadline = models.DateTimeField(verbose_name="Påmeldingsfrist")

    # Deadline for changing your mind
    deregister_deadline = models.DateTimeField(verbose_name="Avmeldingsfrist")

    # Location of event
    location = models.TextField(verbose_name="Sted")

    # Describes the event
    description = models.TextField(verbose_name='Beskrivelse')

    # An image from the event or describing the event
    image = ImageField(upload_to='events', verbose_name="Bilde")

    # Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(default=100, verbose_name="Antall plasser")

    attendees = models.ManyToManyField(User, through='BaseRegistration')

    allowed_grades = ArrayField(
        models.IntegerField(choices=GRADES)
    )

    published = models.BooleanField(default=True, verbose_name='publisert')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_grades_previous = self.allowed_grades

    def __str__(self):
        return self.title

    def get_allowed_grades_display(self):
        return [GRADES.for_value(x).display for x in self.allowed_grades]

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

    def bump_waiting(self):
        if self.waiting_users():
            if self.has_spare_slots:
                attendees = self.attendees.through.objects.filter(status=REGISTRATION_STATUS.WAITING).order_by(
                    'created')[:self.spare_slots]
                for attendee in attendees:
                    attendee.confirm()
                    send_event_mail(attendee, self, self._meta.model_name)

    def registration_has_opened(self):
        return timezone.now() >= self.register_startdate

    @property
    def spare_slots(self):
        return self.sluts - self.registered_users()

    @property
    def has_spare_slots(self):
        return self.spare_slots > 0

    def save(self, *args, **kwargs):
        super(BaseEvent, self).save(*args, **kwargs)
        self.bump_waiting()
        if self.allowed_grades_previous:
            new_grades = set(self.allowed_grades) - set(self.allowed_grades_previous)
            if new_grades:
                # Update all relevant attendees
                self.attendees.through.objects.filter(user__profile__grade__in=new_grades,
                                      status=REGISTRATION_STATUS.INTERESTED). \
                    update(status=REGISTRATION_STATUS.WAITING)
                # Bump once more in case the slot-count was increased as well
                self.bump_waiting()

    def allowed_grade(self, user):
        return user.profile.grade in self.allowed_grades

    class Meta:
        abstract = True


class Social(BaseEvent):
    author = models.ForeignKey(User, related_name='social_author', on_delete=models.CASCADE)
    # Payment information
    payment_information = models.TextField(verbose_name="Betalingsinformasjon", max_length=500)
    price_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, medlem")
    price_not_member = models.PositiveSmallIntegerField(default=0, verbose_name="Pris, ikke-medlem")
    price_companion = models.PositiveSmallIntegerField(default=0, verbose_name="Pris for følge")

    # Boolean fields
    companion = models.BooleanField(default=False, verbose_name="Følge")
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")

    attendees = models.ManyToManyField(User, through='SocialEventRegistration')

    def get_absolute_url(self):
        return reverse('events:detail_social', kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse('events:register_social', kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse('events:delete_social', kwargs={"pk": self.pk})

    def registered_users(self):
        attendees = self.attendees.through.objects.filter(status=REGISTRATION_STATUS.CONFIRMED, event=self)
        attendees_with_companion = attendees.filter(companion__gt='')
        return attendees_with_companion.count() + attendees.count()


class Bedpres(BaseEvent):
    author = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, through='BedpresRegistration')

    def get_absolute_url(self):
        return reverse('events:detail_bedpres', kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse('events:register_bedpres', kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse('events:delete_bedpres', kwargs={"pk": self.pk})


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(BaseEvent, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.INTERESTED)
    arrival_status = models.IntegerField(choices=ARRIVAL_STATUS, default=ARRIVAL_STATUS.NONE)

    objects = RegistrationManager()

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.user.get_full_name(), self.status)

    def confirm(self):
        self.status = REGISTRATION_STATUS.CONFIRMED
        self.save()

    def waiting(self):
        self.status = REGISTRATION_STATUS.WAITING
        self.save()

    class Meta:
        abstract = True
        unique_together = ('event', 'user',)


class SocialEventRegistration(BaseRegistration):
    event = models.ForeignKey(Social, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False, verbose_name="Betalt")

    # Optional fields
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    companion = models.CharField(max_length=40, verbose_name="Navn på eksternt følge",
                                 help_text="Navn på ekstern person. Ønske om bordkavaler sendes til arrangør.",
                                 null=True, blank=True)


class BedpresRegistration(BaseRegistration):
    event = models.ForeignKey(Bedpres, on_delete=models.CASCADE)
    status = models.IntegerField(choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.INTERESTED)


class RegistrationMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)

    # TODO: legge til author
    def __str__(self):
        return '{}, {}: {}'.format(self.event, self.user, self.message)

    class Meta:
        abstract = True


class SocialEventMessage(RegistrationMessage):
    event = models.ForeignKey(Social, related_name='custom_message', on_delete=models.CASCADE)


class BedpresEventMessage(RegistrationMessage):
    event = models.ForeignKey(Bedpres, related_name='custom_message', on_delete=models.CASCADE)