import factory
from ..models import Social


class SocialEvent(factory.DjangoModelFactory):
    class Meta:
        model = Social