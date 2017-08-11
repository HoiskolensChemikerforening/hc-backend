import factory
from django.contrib.auth import models
from .models import Profile, GRADES, RELATIONSHIP_STATUS, FINISH_YEAR, CURRENT_YEAR


class RandomUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('safe_email')
    username = factory.Sequence(lambda n: "user_%d" % n)

    # https://factoryboy.readthedocs.io/en/latest/reference.html#factory.PostGenerationMethodCall
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')
    is_active = True

class RandomProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(RandomUserFactory)

    # https: // faker.readthedocs.io / en / latest / locales / no_NO.html
    grade = factory.Iterator(GRADES)
    start_year = CURRENT_YEAR
    end_year = FINISH_YEAR
    allergies = factory.Faker('lorem', nb_words=6, variable_nb_words=True, ext_word_list=None)
    relationship_status = factory.Iterator(RELATIONSHIP_STATUS)
    phone_number = factory.Faker('phone_number')
    access_card = factory.Faker('password', legth=10)

    image_primary = factory.django.ImageField(color='blue')
    image_secondary = factory.django.ImageField(color='red')
    address = factory.Faker('address')
