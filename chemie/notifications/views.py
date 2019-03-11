from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required, permission_required
from push_notifications.models import APNSDevice, GCMDevice
from .models import Device, CoffeeSubmission
from django.views.decorators.csrf import csrf_exempt
import os
import json
from rest_framework import viewsets
from .serializers import CoffeeSubmissionSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



class CoffeeSubmissionViewSet(viewsets.ModelViewSet):
    queryset = CoffeeSubmission.objects.all().order_by('date')
    serializer_class = CoffeeSubmissionSerializer


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
    if request.method == 'GET':
        submissions = CoffeeSubmission.objects.all()
        serializer = CoffeeSubmissionSerializer(submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        payload_bytes = request.body
        payload_bytes_decoded = payload_bytes.decode('utf8')
        payload_json = json.loads(payload_bytes_decoded)
        serializer = CoffeeSubmissionSerializer(data=payload_json)
        if serializer.is_authorized(
            payload_json['notification_key'], 
            payload_json['topic']
            ):
            if CoffeeSubmission.check_last_submission():
                serializer.save()

                gcm_devices = Device.objects.filter(coffee_subscription=True, gcm_device__active=True)
                [device.send_notification("Kaffe", "Nytraktet kaffe på kontoret") for device in gcm_devices]
            return JsonResponse(serializer.errors, status=201)
        return JsonResponse(serializer.errors, status=401)
    return redirect(reverse('frontpage:home'))
