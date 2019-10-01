from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from sorl.thumbnail import ImageField
from django.conf import settings
from audiofield.fields import AudioField


class Podcast(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(verbose_name="beskrivelse", config_name="news")
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="Images", verbose_name="Bilde")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name="Publisert")
    audio_file = AudioField(upload_to='your/upload/dir', blank=True,
                            ext_whitelist=(".mp3", ".wav", ".ogg"),
                            help_text="Allowed type - .mp3, .wav, .ogg")
    url_number = models.URLField(
        name="Url Number",
        max_length=128,
        db_index=True,
        unique=True,
        blank=True
    )

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (
                file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = 'Audio file player'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sugepodden:detail_podcast", kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse("sugepodden:register_podcast", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse("sugepodden:delete_podcast", kwargs={"pk": self.pk})
