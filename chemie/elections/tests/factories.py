import factory

from chemie.elections.models import Position


class PositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Position

    position_name = factory.Faker("first_name")
    spots = 2
