import factory

from chemie.customprofile.factories import RandomUserFactory, RandomUserWithProfileFactory, RandomProfileFactory
from chemie.elections.models import Position, Candidates


class PositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Position
    position_name = factory.Faker('first_name')
    spots = 2


class CandidateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Candidates
    candidate_user = factory.SubFactory(RandomUserFactory)