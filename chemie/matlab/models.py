from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField() #1kg løk og 1stk løk vil være to ingredienser... løk er jo løk
    unit = models.CharField(max_length=100)

    
    def __str__(self):
        return f"{self.name}"

class Kategori(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"

class Recipes(models.Model):
    name = models.CharField(max_length=30)
    price = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField()
    ingredients = models.ManyToManyField(Ingredients, blank = True)
    categories = models.ManyToManyField(Kategori, blank=True)

    def __str__(self):
        return f"{self.name}"


#class Korv(models.Model):
#    weight = models.DecimalField(decimal_places=2, max_digits=8)
#    length = models.DecimalField(decimal_places=2, max_digits=8)
#    name = models.CharField(max_length=30)
#    boar = models.ForeignKey(Villsvin, on_delete=models.CASCADE)


#    def __str__(self):
#        return f"{self.name} {self.weight}"