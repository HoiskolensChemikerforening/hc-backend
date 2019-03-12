from django.contrib import admin
from .models import Device,CoffeeSubmission
from django.contrib import admin
from push_notifications.models import APNSDevice, GCMDevice


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('gcm_device', 'coffee_subscription', 'news_subscription')



@admin.register(CoffeeSubmission)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('date',)

