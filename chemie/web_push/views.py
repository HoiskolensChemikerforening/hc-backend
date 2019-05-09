from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from push_notifications.models import GCMDevice, APNSDevice
from .models import Device, CoffeeSubmission
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from .serializers import CoffeeSubmissionSerializer
from django.http import HttpResponse, JsonResponse


class CoffeeSubmissionViewSet(viewsets.ModelViewSet):
    queryset = CoffeeSubmission.objects.order_by("date")
    serializer_class = CoffeeSubmissionSerializer


@login_required
def save_device(request):
    """ Creates a device and gcm/apns device for user that allowes for notification """
    if request.method == "POST":
        browser = request.POST["browser"]
        token = request.POST["token"]
        if browser is not None and token != "":
            if browser == "Chrome":
                registered_device = GCMDevice.objects.filter(
                    registration_id=token
                )
                if registered_device.count() == 0:
                    gcm_device = GCMDevice.objects.create(
                        registration_id=token,
                        cloud_message_type="FCM",
                        user=request.user,
                    )
                    Device.objects.create(
                        owner=request.user, gcm_device=gcm_device
                    )
                    users_devices = Device.objects.filter(owner=request.user)
                    if len(users_devices) > 5:
                        users_devices.latest("-date_created").delete()
                    return HttpResponse(status=201)

            """
            The commented lines below is the implementation for Safari browser
            Apples APNS certificat would be needed, cost ~1000 NOK/year
            The code has not been testet so no garanties it would work
            """
            # elif browser == "Safari":
            #     registered_device = APNSDevice.objects.filter(
            #         registration_id=token
            #     )
            #     if len(registered_device) == 0:
            #         apns_device = APNSDevice.objects.create(
            #             registration_id=token, user=request.user
            #         )
            #         Device.objects.create(
            #             owner=request.user, apns_device=apns_device
            #         )
            #         users_devices = Device.objects.filter(owner=request.user)
            #         if len(users_devices) > 5:
            #             users_devices.latest("-date_created").delete()
            #         return HttpResponse(status=201)
        return HttpResponse(status=301)
    else:
        return redirect(reverse("frontpage:home"))


@csrf_exempt
def send_notification(request):
    """ Send notification to all users from notification/send url """
    if request.method == "POST":
        payload_bytes = request.body
        payload_bytes_decoded = payload_bytes.decode("utf8")
        payload_json = json.loads(payload_bytes_decoded)
        serializer = CoffeeSubmissionSerializer(data=payload_json)

        is_authorized = serializer.is_authorized(
            payload_json["notification_key"], payload_json["topic"]
        )
        if is_authorized:
            if CoffeeSubmission.fifteen_minutes_has_passed():
                serializer.save()

                gcm_devices = Device.objects.filter(
                    coffee_subscription=True, gcm_device__active=True
                )
                [
                    device.send_notification(
                        "Kaffe", "Nytraktet kaffe på kontoret"
                    )
                    for device in gcm_devices
                ]

                """
                The commented lines below is the implementation for Safari browser
                Apples APNS certificat would be needed, cost ~1000 NOK/year
                The code has not been testet so no garanties it would work
                """
                # apns_devices = Device.objects.filter(
                #     coffee_subscription=True, apns_device__active=True
                # )
                # [
                #     device.send_notification(
                #         "Kaffe", "Nytraktet kaffe på kontoret"
                #     )
                #     for device in apns_devices
                # ]
            return JsonResponse(serializer.errors, status=201)
        return JsonResponse(serializer.errors, status=401)
    else:  # PUT eller DELETE request
        return redirect(reverse("frontpage:home"))
