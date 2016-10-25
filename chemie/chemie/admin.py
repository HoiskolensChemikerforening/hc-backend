from django.contrib import admin
from .models import  pictures_for_404
from chemie.models import Sponsor


admin.site.register(pictures_for_404)
admin.site.register(Sponsor)
