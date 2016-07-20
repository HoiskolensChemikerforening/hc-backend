from django.db import models
from datetime import datetime
from sorl.thumbnail import ImageField

# Create your models here.
class Event(models.Model):
    #Name of the event
    title = models.CharField(max_length=40)
    #When the event actually occurs
    date = models.DateTimeField(default=datetime.now())
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    #Start time for registration
    register_startdate = models.DateField(default=datetime.now())
    #Deadline for signing up
    register_deadline=models.DateField(default=datetime.now())
    #Deadline for changing your mind
    deregister_deadline=models.DateField(default=datetime.now())
    #Location of event
    location = models.TextField()
    #Describes the event
    description = models.TextField()
    #An image from the event or describing the event
    image = ImageField(upload_to='events')
    #Number of slots reserved for the event
    sluts = models.PositiveSmallIntegerField(default=100)
    #Payment information
    payment_information = models.TextField()
    price_member = models.PositiveSmallIntegerField(default=0)
    price_not_member = models.PositiveSmallIntegerField(default=0)
    price_companion = models.PositiveSmallIntegerField(default=0)
    #Boolean fields
    companion = models.BooleanField(default=False)
    sleepover = models.BooleanField(default=False)
    night_snack = models.BooleanField(default=False)
    mail_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.title
