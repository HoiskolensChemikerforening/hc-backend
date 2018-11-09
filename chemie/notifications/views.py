from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required, permission_required
from push_notifications.models import APNSDevice, GCMDevice
from .models import Device
# Create your views here.

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

@login_required
@permission_required('notifications.add_notification')
def send_notification(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        if topic == "coffee":
            devices = Device.objects.filter(coffee_subscription=True)
            devices.send_notification("Kaffe", "Nytraktet kaffe på kontoret")
        elif topic == "news":
            message = request.post['message']
            devices = Device.objects.filter(news_subscription=True)
            devices.send_notification("Nyheter", message)
    return redirect(reverse('frontpage:home'))
