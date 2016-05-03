from django.db import models

# Create your models here.
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.contrib.auth.models import User

"""
class ProfileImage(models.Model):
    avatar = models.ImageField(upload_to='static')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(180, 250)],
                                      format='PNG',
                                      options={'quality': 60})
    def __str__(self):
        return (str(self.avatar))
"""

class Profile(models.Model):
    first_name = models.CharField(max_length=30, null = True)
    last_name = models.CharField(max_length=30, null = True)
    username = models.ForeignKey(User, null = True)
    image = models.FileField(null=True, blank=True)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return(self.last_name + ", " + self.first_name)






#profile = ProfileImage.objects.all()[0]
#print(profile.avatar_thumbnail.url)    # > /media/CACHE/images/982d5af84cddddfd0fbf70892b4431e4.jpg
#print(profile.avatar_thumbnail.width)  # > 100
