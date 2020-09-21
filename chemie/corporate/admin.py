from django.contrib import admin
from .models import Specialization, Interview, JobAdvertisement


admin.site.register(Interview)
admin.site.register(Specialization)
admin.site.register(JobAdvertisement)
