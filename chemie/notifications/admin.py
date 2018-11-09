from django.contrib import admin
from .models import Device
from django.contrib import admin
from push_notifications.models import APNSDevice, GCMDevice



class DeviceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Subscriptions', {'fields': ['coffee_subscription','news_subscription']}),
        ('GCM Device',{'fields': ['gcm_device']})
    ]

admin.site.register(Device, DeviceAdmin)

