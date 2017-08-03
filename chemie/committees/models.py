from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from sorl.thumbnail import ImageField


class Committee(models.Model):
    title = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    image = ImageField(upload_to='komiteer')
    slug = models.SlugField(null=True, blank=True)
    one_liner = models.CharField(max_length=30, verbose_name="Lynbeskrivelse")
    description = RichTextField(verbose_name='Beskrivelse', config_name='committees')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('verv:committee_detail', kwargs={'slug': self.slug})


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="Stillingsnavn")
    email = models.EmailField(null=True, blank=True, verbose_name="Epost")
    committee = models.ForeignKey(Committee, )
    permission_group = models.ForeignKey(Group)
    max_members = models.PositiveSmallIntegerField(default=1, verbose_name='Antall medlemmer')
    can_manage_committee = models.BooleanField(default=False)
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name='medlem')

    def remove_from_group(self, users):
        for user in users:
            self.permission_group.user_set.remove(user)

    def add_to_group(self, users):
        for user in users:
            self.permission_group.user_set.add(user)

    # Signal for adding and removing users from a permission group as they are added/removed to a Position
    # https://stackoverflow.com/a/4571362
    @staticmethod
    def consistent_permissions(sender, instance, action, reverse, model, pk_set, **kwargs):
        if action == 'post_add':
            instance.add_to_group(instance.users.all())
        elif action == 'pre_remove':
            instance.remove_from_group(instance.users.all())

    def __str__(self):
        return str(self.title)


@receiver(pre_delete, sender=Position)
def update_position_member_groups_on_delete(sender, instance, *args, **kwargs):
    instance.remove_from_group(instance.users.all())


@receiver(pre_save, sender=Committee)
def pre_save_committee_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


m2m_changed.connect(receiver=Position.consistent_permissions, sender=Position.users.through)
