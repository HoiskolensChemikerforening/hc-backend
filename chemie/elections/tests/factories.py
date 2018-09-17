from chemie.customprofile.factories import RandomUserFactory
import factory
from chemie.elections.models import Position, Candidates
import random


class PositionFactory(factory.DjangoModelFactory):
    class Meta:
        model=Position
    position_name = factory.Faker('first_name')
    spots = random.randint(1,5)


class CandidateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Candidates
    candidate_user = factory.SubFactory(RandomUserFactory)