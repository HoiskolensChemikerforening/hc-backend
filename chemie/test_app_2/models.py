from django.db import models
from sorl.thumbnail import ImageField

class Cult(models.Model):
    name = models.CharField(max_length=2000, verbose_name="Cult name")
    cover = ImageField(
        upload_to="shitbox", blank=True, null=True, verbose_name="Cover"
    )
    motto=models.TextField(max_length=2000)
    date = models.DateTimeField(verbose_name="Dato")
    #lager en cult med dato culten er laget, og et bilde

class Role(models.Model):
    Role = models.CharField()

class Executive(models.Model):
    Is_executive=models.BooleanField()
    executive = models.ManyToOneRel(Cult, blank=True, on_delete=models.CASACADE)

class Bruker(models.Model):
    navn=models.CharField(max_length=1000)
    age=models.PositiveIntegerField()
    er_leder=models.OneToOneField(Role, blank=True, on_delete=models.do_nothing)
    dead=models.BooleanField(default=False)
    tilhører=models.ForeignKey(Cult, on_delete=models.CASCADE)


class Sacrifice(models.Model):
    navn=models.CharField(max_length=1000)
    age=models.DateTimeField()
    used=models.BooleanField(default=False)
    sacrifices=models.ManyToOneRel(Cult, blank=True, on_delete=models.CASCADE)

class Gold(models.Model):
    amount=models.PositiveIntegerField()
    gold=models.OneToOneField(Cult, on_delete=models.CASCADE)