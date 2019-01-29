from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required, permission_required
from push_notifications.models import APNSDevice, GCMDevice
from .models import Device, CoffeeSubmission
from django.views.decorators.csrf import csrf_exempt
import os


@login_required
def edit_notifications(request):
    return render(request, 'editnotifications.html')

@login_required
def save_device(request):
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
    try:
        if request.method == 'POST':
            if request.POST['notification_key'] == os.environ.get('NOTIFICATION_KEY'):
                topic = request.POST['topic']
                if topic == "coffee":
                    if CoffeeSubmission.check_last_submission():
                        gcm_devices = Device.objects.filter(coffee_subscription=True, gcm_device__active=True)
                        # TODO create batch send
                        [device.send_notification("Kaffe", "Nytraktet kaffe på kontoret") for device in gcm_devices]
                        CoffeeSubmission.objects.create()
                elif topic == "news":
                    message = request.post['message']
                    gcm_devices = Device.objects.filter(news_subscription=True,gcm_device__active=True)
                    [device.send_notification("Nyheter", message) for device in gcm_devices]
            else:
                raise ConnectionAbortedError('Notification key is not valid')
    except ConnectionAbortedError:
        pass
    return redirect(reverse('frontpage:home'))
