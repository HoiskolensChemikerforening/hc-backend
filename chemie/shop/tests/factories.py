from decimal import Decimal

import factory
from django.template.defaultfilters import slugify

from chemie.shop.models import Item, Category


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category
        # Deal with name is unique constraint
        django_get_or_create = ('name',)

    name = factory.Faker("first_name")
    slug = slugify(name)


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = Item
        # Deal with name is unique constraint
        django_get_or_create = ('name',)

    name = factory.Faker("first_name")
    price = Decimal(2)
    description = factory.Faker("last_name")
    category = factory.SubFactory(CategoryFactory)
    image = factory.django.ImageField(color="red")
