import factory
import decimal

from django.template.defaultfilters import slugify
from chemie.shop.models import Item, Category


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("first_name")
    slug = slugify(name)


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker("first_name")
    price = decimal(2)
    description = factory.Faker("last_name")
    category = factory.SubFactory(CategoryFactory)
    image = factory.django.ImageField(color="red")
