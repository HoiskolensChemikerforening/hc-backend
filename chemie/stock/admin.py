from django.contrib import admin

# Register your models here.

from .models import Stocktype, Stock, History, Portfolio

admin.site.register(Stock)
admin.site.register(Stocktype)
admin.site.register(Portfolio)
admin.site.register(History)
