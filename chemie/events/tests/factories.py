import factory

from customprofile.factories import RandomUserFactory
from ..models import Bedpres, Social
from django.utils import timezone
from datetime import timedelta

def now_offset_days(days=0):
    return timezone.now() + timedelta(days=days)

class BaseEventFactory(factory.DjangoModelFactory):
    title = 'Event Title'
    author = factory.SubFactory(RandomUserFactory)
    location = 'Event Location'
    description = 'Event Description'
    image = factory.django.ImageField(color='red')

    register_startdate = factory.LazyFunction(lambda: now_offset_days(2))
    register_deadline = factory.LazyFunction(lambda: now_offset_days(4))
    deregister_deadline = factory.LazyFunction(lambda: now_offset_days(6))
    date = factory.LazyFunction(lambda: now_offset_days(8))
    sluts = 10
    allowed_grades = [1, 2, 3, 4, 5, 6]


class BedpresEventFactory(BaseEventFactory):
    class Meta:
        model = Bedpres


class SocialEventFactory(BaseEventFactory):
    payment_information = 'Social event payment information'
    price_member = 101
    price_not_member = 202
    price_companion = 153

    class Meta:
        model = Social
