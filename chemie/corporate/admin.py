from django.contrib import admin
from .models import Specialization, Interview, Job

admin.site.register(Interview)
admin.site.register(Specialization)
admin.site.register(Job)
