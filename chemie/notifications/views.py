from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required, permission_required
from push_notifications.models import APNSDevice, GCMDevice
from .models import Device, CoffeeSubmission
from django.views.decorators.csrf import csrf_exempt
import os
import json

@login_required
def save_device(request):
    """ Creates a device and gcm/apns device for user that allowes for notification """
    if request.method == "POST":
        browser = request.POST['browser']
        token = request.POST['token']
        if browser is not None and token is not '':
            if GCMDevice.objects.filter(registration_id=token).count() == 0:
                device = GCMDevice.objects.create(registration_id=token, cloud_message_type="FCM", user=request.user)
                Device.objects.create(gcm_device=device)  # saving device token with user
    return redirect(reverse('frontpage:home'))


@csrf_exempt
def send_notification(request):
    """ Send notification to all users from notification/send url """
    if request.method == 'POST':
        payload_bytes = request.body
        payload_bytes_decoded = payload_bytes.decode('utf8').replace("'", '"')
        payload_json = json.loads(payload_bytes_decoded)

        # Custom symmetric verification key. One is storred on device with identical on server
        if payload_json['notification_key'] == os.environ.get('NOTIFICATION_KEY'):
            topic = payload_json['topic']
            if topic == "coffee":

                # Prevent to frequent notification sendings
                if CoffeeSubmission.check_last_submission():
                    gcm_devices = Device.objects.filter(coffee_subscription=True, gcm_device__active=True)
                    [device.send_notification("Kaffe", "Nytraktet kaffe på kontoret") for device in gcm_devices]
                    CoffeeSubmission.objects.create()

            # Redundant method which may be implemented later
            elif topic == "news":
                message = request.post['message']
                gcm_devices = Device.objects.filter(news_subscription=True,gcm_device__active=True)
                [device.send_notification("Nyheter", message) for device in gcm_devices]
        else:
            raise ConnectionAbortedError('Notification key is not valid')
    return redirect(reverse('frontpage:home'))
