from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db import models
from django.utils import timezone
from extended_choices import Choices
from sorl.thumbnail import ImageField

from chemie.customprofile.models import GRADES
from chemie.committees.models import Committee
from .email import send_event_mail

from django.db import transaction


REGISTRATION_STATUS = Choices(
    ("CONFIRMED", 1, "Confirmed"),
    ("WAITING", 2, "Waiting"),
    ("INTERESTED", 3, "Interested"),
    ("SOLD", 4, "Sold"),
    ("INACTIVE", 5, "Inactive"),
    ("OFFERED", 6, "Offered"),
)

ARRIVAL_STATUS = Choices(
    ("NONE", 1, "Ikke satt"),
    ("PRESENT", 2, "Møtt"),
    ("TRUANT", 3, "Ikke møtt"),
)


class BaseEvent(models.Model):
    # Name of the event
    title = models.CharField(max_length=40, verbose_name="Tittel")

    # Name of person creating event
    author = models.ForeignKey(
        User, related_name="baseevent", on_delete=models.CASCADE
    )

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
    description = models.TextField(verbose_name="Beskrivelse")

    # An image from the event or describing the event
    image = ImageField(upload_to="events", verbose_name="Bilde")

    # Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Antall plasser, sett til 0 for åpent arrangement",
    )

    attendees = models.ManyToManyField(User, through="BaseRegistration")

    allowed_grades = ArrayField(models.IntegerField(choices=GRADES))

    published = models.BooleanField(default=True, verbose_name="publisert")

    tentative = models.BooleanField(default=False, verbose_name="tentativ")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_grades_previous = self.allowed_grades

    def __str__(self):
        return self.title

    def get_allowed_grades_display(self):
        if len(self.allowed_grades) > 4:
            return ["Alle"]
        else:
            return [GRADES.for_value(x).display for x in self.allowed_grades]

        # Makes nicer view on detalis page.

    def registered_users(self):
        return self.attendees.through.objects.filter(
            status=REGISTRATION_STATUS.CONFIRMED, event=self
        ).count()

    def waiting_users(self):
        return self.attendees.through.objects.filter(
            status=REGISTRATION_STATUS.WAITING, event=self
        ).count()

    @property
    def can_signup(self):
        return (timezone.now() >= self.register_startdate) and (
            timezone.now() <= self.register_deadline
        )

    @property
    def can_de_register(self):
        return timezone.now() <= self.deregister_deadline

    def percentage_filled(self):
        try:
            return round((self.registered_users() / self.sluts) * 100)
        except ZeroDivisionError:
            return "N/A"

    def bump_waiting(self):
        if self.waiting_users():
            if self.has_spare_slots:
                attendees = self.attendees.through.objects.filter(
                    event=self, status=REGISTRATION_STATUS.WAITING
                ).order_by("created")[: self.spare_slots]
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
        super().save(*args, **kwargs)
        self.bump_waiting()
        if self.allowed_grades_previous:
            new_grades = set(self.allowed_grades) - set(
                self.allowed_grades_previous
            )
            if new_grades:
                # Update all relevant attendees
                self.attendees.through.objects.filter(
                    user__profile__grade__in=new_grades,
                    status=REGISTRATION_STATUS.INTERESTED,
                ).update(status=REGISTRATION_STATUS.WAITING)
                # Bump once more in case the slot-count was increased as well
                self.bump_waiting()

    def allowed_grade(self, user):
        return user.profile.grade in self.allowed_grades

    class Meta:
        abstract = True


class Social(BaseEvent):
    author = models.ForeignKey(
        User, related_name="social_author", on_delete=models.CASCADE
    )
    #   Name of the committee responsible for the event
    committee = models.ForeignKey(
        Committee, null=True, blank=True, on_delete=models.CASCADE
    )
    # Payment information
    payment_information = models.TextField(
        verbose_name="Betalingsinformasjon", max_length=500
    )
    price_member = models.PositiveSmallIntegerField(
        default=0, verbose_name="Pris, medlem"
    )
    price_not_member = models.PositiveSmallIntegerField(
        default=0, verbose_name="Pris, ikke-medlem"
    )
    price_companion = models.PositiveSmallIntegerField(
        default=0, verbose_name="Pris for følge"
    )

    # Boolean fields
    companion = models.BooleanField(default=False, verbose_name="Følge")
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    check_in = models.BooleanField(default=False, verbose_name="Innsjekking")

    attendees = models.ManyToManyField(User, through="SocialEventRegistration")

    def get_absolute_url(self):
        return reverse("events:detail_social", kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse("events:register_social", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse("events:delete_social", kwargs={"pk": self.pk})

    def registered_users(self):
        attendees = self.attendees.through.objects.filter(
            status=REGISTRATION_STATUS.CONFIRMED, event=self
        )
        attendees_with_companion = attendees.filter(companion__gt="")
        return attendees_with_companion.count() + attendees.count()

    def get_model_type(self):
        return "social"

    def get_queue_position(self, user):
        user_reg = (
            self.socialeventregistration_set.all().filter(user=user).first()
        )
        return SocialEventRegistration.get_queue_position(user_reg)


class Bedpres(BaseEvent):
    author = models.ForeignKey(
        User, related_name="+", on_delete=models.CASCADE
    )
    attendees = models.ManyToManyField(User, through="BedpresRegistration")

    def get_absolute_url(self):
        return reverse("events:detail_bedpres", kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse("events:register_bedpres", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse("events:delete_bedpres", kwargs={"pk": self.pk})

    def get_model_type(self):
        return "bedpres"

    def get_queue_position(self, user):
        user_reg = self.bedpresregistration_set.all().filter(user=user).first()
        return BedpresRegistration.get_queue_position(user_reg)


class RegistrationManager(models.Manager):
    def de_register(self, reg_to_be_deleted):
        event = reg_to_be_deleted.event
        reg_to_be_deleted.delete()
        waiting = self.filter(event=event, status=REGISTRATION_STATUS.WAITING)
        if waiting:
            if event.has_spare_slots:
                sorted_waiting = waiting.order_by("created")
                lucky_person = sorted_waiting[0]
                lucky_person.confirm()
                return lucky_person


class BaseRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(BaseEvent, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.INTERESTED
    )
    arrival_status = models.IntegerField(
        choices=ARRIVAL_STATUS,
        default=ARRIVAL_STATUS.NONE,
        verbose_name="Oppmøtestatus",
    )

    objects = RegistrationManager()

    def __str__(self):
        return "{} - {} - {}".format(
            self.event, self.user.get_full_name(), self.status
        )

    def confirm(self):
        self.status = REGISTRATION_STATUS.CONFIRMED
        self.save()

    def waiting(self):
        self.status = REGISTRATION_STATUS.WAITING
        self.save()

    def sold(self):
        self.status = REGISTRATION_STATUS.SOLD
        self.save()

    def inactivate(self):
        self.status = REGISTRATION_STATUS.INACTIVE
        self.save()

    def offered(self):
        self.status = REGISTRATION_STATUS.OFFERED
        self.save()

    @classmethod
    def get_queue_position(cls, registration):
        # Finner plass på ventiliste eller none om ikke
        queue_position = None
        if registration.status == REGISTRATION_STATUS.WAITING:
            queue_position = (
                cls.objects.filter(
                    event=registration.event,
                    created__lt=registration.created,
                    status=REGISTRATION_STATUS.WAITING,
                ).count()
                + 1
            )
        return queue_position

    class Meta:
        abstract = True
        unique_together = ("event", "user")


class SocialEventRegistration(BaseRegistration):
    event = models.ForeignKey(Social, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False, verbose_name="Betalt")

    # Optional fields
    sleepover = models.BooleanField(default=False, verbose_name="Overnatting")
    night_snack = models.BooleanField(default=False, verbose_name="Nattmat")
    companion = models.CharField(
        max_length=40,
        verbose_name="Navn på eksternt følge",
        help_text="Navn på ekstern person. Ønske om bordkavaler sendes til arrangør.",
        null=True,
        blank=True,
    )


class BedpresRegistration(BaseRegistration):
    event = models.ForeignKey(Bedpres, on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=REGISTRATION_STATUS.INTERESTED
    )


class RegistrationMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(
        User, related_name="+", on_delete=models.CASCADE
    )

    # TODO: legge til author
    def __str__(self):
        return "{}, {}: {}".format(self.event, self.user, self.message)

    class Meta:
        abstract = True


class SocialEventMessage(RegistrationMessage):
    event = models.ForeignKey(
        Social, related_name="custom_message", on_delete=models.CASCADE
    )


class BedpresEventMessage(RegistrationMessage):
    event = models.ForeignKey(
        Bedpres, related_name="custom_message", on_delete=models.CASCADE
    )


class BaseResellReceipt(models.Model):

    resell_payment_status = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    

    # Time data
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    response_time = models.DurationField() 
    deadline = models.DateTimeField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        """Override save to calculate the deadline when the model is saved."""
        if self.response_time and self.edited:
            self.deadline = self.edited + self.response_time  
        super().save(*args, **kwargs)  


    class Meta:
        abstract = True

class SocialResellReceipt(BaseResellReceipt):
    seller_registration = models.OneToOneField(SocialEventRegistration, on_delete=models.CASCADE, related_name='sosial_resell_receipt_seller')
    buyer_registration = models.OneToOneField(SocialEventRegistration, on_delete=models.SET_NULL, blank=True, null=True, related_name='sosial_resell_receipt_buyer') 

    @transaction.atomic
    def offer(self):
        """
        Get a new buyer from the queue as long as there are candidates in the queue
        """
        event = self.seller_registration.event
        if self.buyer_registration:
            self.buyer_registration.inactivate()
        waiting = SocialEventRegistration.objects.filter(event=event, status=REGISTRATION_STATUS.WAITING)
        if waiting:
            candidate_registration = waiting.order_by("created")[0]
            candidate_registration.offered()
            self.buyer_registration = candidate_registration
            self.save()


        # Send e-mail to offer a ticket

    def save(self, *args, **kwargs):
        """Override save to offer to the first person in the queue."""
        if not self.buyer_registration:
            event = self.seller_registration.event
            waiting = SocialEventRegistration.objects.filter(event=event, status=REGISTRATION_STATUS.WAITING)
            if waiting:
                candidate_registration = waiting.order_by("created")[0]
                candidate_registration.offered()
                self.buyer_registration = candidate_registration

        super().save(*args, **kwargs)  
    
    def buy(self):
        self.sold = True
        self.save()
        #Send e-mail to ask for confirming the payment

    
    @transaction.atomic
    def sell(self):
        self.seller_registration.inactivate()
        self.buyer_registration.confirm()
    
    def confirm_payment(self):
        self.resell_payment_status = True
        self.save()
        self.sell()
        # Send confirmation e-mail





        



