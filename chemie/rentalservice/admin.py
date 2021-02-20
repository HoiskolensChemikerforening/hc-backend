from django.contrib import admin
from .models import RentalObject, Landlord, Invoice


admin.site.register(RentalObject)
admin.site.register(Landlord)
admin.site.register(Invoice)
