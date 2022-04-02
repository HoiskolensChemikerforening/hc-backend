from django.contrib import admin
from .models import Merch, MerchCategory
# Register your models here.

admin.site.register(Merch)
admin.site.register(MerchCategory)