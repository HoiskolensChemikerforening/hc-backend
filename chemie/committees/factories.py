import factory
from django.contrib.auth.models import Group, Permission

from .models import Committee, Position


class PermissionGroup(factory.DjangoModelFactory):
    class Meta:
        model = Group

    # http://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    def _add_permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for perm in extracted:
                self.permissions.add(perm)

            self.save()


class HighAccessGroup(PermissionGroup):
    name = 'Admins'

    @factory.post_generation
    def groups(self, create, extracted=None, **kwargs):
        if not extracted:
            extracted = Permission.objects.filter(codename__in=[
                'change_committee', 'add_committee', 'add_position'])
        PermissionGroup._add_permissions(self, create, extracted, **kwargs)


class LowAccessGroup(PermissionGroup):
    name = 'Regular'

    @factory.post_generation
    def groups(self, create, extracted=None, **kwargs):
        if not extracted:
            extracted = Permission.objects.filter(codename='change_committee')
        PermissionGroup._add_permissions(self, create, extracted, **kwargs)


class RandomCommitteeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Committee

    title = factory.Faker('word')
    email = factory.Faker('safe_email')
    image = factory.django.ImageField(color='green')
    one_liner = factory.Faker('text', max_nb_chars=30)
    description = factory.Faker('sentences', nb=3)


class RandomBasePositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker('word')
    email = factory.Faker('safe_email')
    committee = factory.SubFactory(RandomCommitteeFactory)
    max_members = factory.Iterator([2, 3])


class HighPermissionPositionFactory(RandomBasePositionFactory):
    permission_group = factory.SubFactory(HighAccessGroup)
    max_members = 2


class LowPermissionPositionFactory(RandomBasePositionFactory):
    permission_group = factory.SubFactory(LowAccessGroup)
    max_members = 1
