from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from smart_selects.db_fields import ChainedForeignKey
from sorl.thumbnail import ImageField

from customprofile.models import Profile


class Committee(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    image = ImageField(upload_to='kommiteer')

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="Stillingsnavn")
    email = models.EmailField(null=True, blank=True, verbose_name="Epost")
    committee = models.ForeignKey(Committee)
    permission_group = models.ForeignKey(Group)

    def __str__(self):
        return str(self.position_name)


class Member(models.Model):
    committee = models.ForeignKey(Committee)
    position = ChainedForeignKey(
        Position,
        chained_field="committee",
        chained_model_field="committee",
        show_all=False,
        auto_choose=True
    )
    user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return "Ledig"

    def remove_from_group(self, user):
        self.position.permission_group.user_set.remove(user)

    def add_to_group(self, user):
        self.position.permission_group.user_set.add(user)

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self.initial_user = self.user

    def save(self, *args, **kwargs):
        if self.pk:
            old = Member.objects.get(pk=self.pk).user
            self.remove_from_group(old)
        if self.user:
            self.add_to_group(self.user)
        super(Member, self).save()


@receiver(pre_delete, sender=Member)
def update_position_member_groups_on_save(sender, instance, *args, **kwargs):
    instance.remove_from_group(instance.user)
