import factory
from django.contrib.auth import models

from .models import (
    Profile,
    GRADES,
    RELATIONSHIP_STATUS,
    SPECIALIZATION,
    FINISH_YEAR,
    CURRENT_YEAR,
)


class RandomUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("safe_email")
    username = factory.Sequence(lambda n: "user_%d" % n)

    # https://factoryboy.readthedocs.io/en/latest/reference.html#factory.PostGenerationMethodCall
    password = factory.PostGenerationMethodCall(
        "set_password", "defaultpassword"
    )
    is_active = True


class RandomProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(RandomUserFactory)

    # https: // faker.readthedocs.io / en / latest / locales / no_NO.html
    grade = factory.Iterator(GRADES.values.keys())
    start_year = CURRENT_YEAR
    end_year = FINISH_YEAR
    allergies = factory.Sequence(lambda n: "Allergen_%d" % n)
    relationship_status = factory.Iterator(RELATIONSHIP_STATUS.values.keys())
    specialization = factory.Iterator(SPECIALIZATION.values.keys())
    phone_number = factory.sequence(lambda p: p)
    access_card = factory.Faker("password", length=10)

    image_primary = factory.django.ImageField(color="blue")
    image_secondary = factory.django.ImageField(color="red")
    address = factory.Faker("address")
    approved_terms = True
