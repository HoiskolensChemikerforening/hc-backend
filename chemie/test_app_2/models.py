from django.db import models
from sorl.thumbnail import ImageField

class Role(models.Model):
    Role = models.CharField()

class Executive(models.Model):
    Is_executive=models.BooleanField()

class Bruker(models.Model):
    navn=models.CharField(max_length=1000)
    age=models.PositiveIntegerField()
    er_leder=models.OneToOneField(Role, blank=True)
    Dead=models.BooleanField(default=False)

class Sacrifice(models.Model):
    navn=models.CharField(max_length=1000)
    age=models.DateTimeField()
    used=models.BooleanField(default=False)

class Gold(models.Model):
    amount=models.PositiveIntegerField()


class Cult(models.Model):
    content = models.TextField(max_length=2000, verbose_name="Title")
    cover = ImageField(
        upload_to="shitbox", blank=True, null=True, verbose_name="Cover"
    )
    date = models.DateTimeField(verbose_name="Dato")
    executive = models.ManyToOneRel(Executive, blank=True)
    sacrifices=models.ManyToOneRel(Sacrifice, blank=True)
    gold=models.OneToOneField(Gold)
    


