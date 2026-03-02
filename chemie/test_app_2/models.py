from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

class Participant:
    def __init__(self, name, level):
        self.name = name
        self.level = level # Depth in the pyramid
        self.recruiter = None
        self.subordinates = []
        self.invested = 1000 # Cost to join 

    def recruit(self, new_person):
        new_person.recruiter = self
        self.subordinates.append(new_person)
        print(f"{self.name} recruited {new_person.name}")

    def calculate_profit(self):
        # Profit = Money from subordinates - Money paid up
        subordinate_income = len(self.subordinates) * 500
        return subordinate_income - self.invested

class Member(models.Model):
    name = models.CharField(max_length=100)
    image = ImageField(upload_to="the boss", blank=True, null=True, verbose_name="Bilde")
    content = models.TextField(max_length=2000, verbose_name="Sladre på motstandere")
    when_created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="When_tf_joined?")

    

    # The recruiter (parent) who brought this person in
    recruiter = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='recruits'

    
    )
    investment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name






