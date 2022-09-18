from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from push_notifications.models import GCMDevice, APNSDevice
from .models import Device, CoffeeSubmission, Subscription
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from .serializers import CoffeeSubmissionSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
import datetime


class CoffeeSubmissionViewSet(viewsets.ModelViewSet):
    queryset = CoffeeSubmission.objects.order_by("date")
    serializer_class = CoffeeSubmissionSerializer


@login_required
def save_device(request):
    """Creates a device and gcm/apns device for user that allowes for notification"""
    if request.method == "POST":
        browser = request.POST["browser"]
        token = request.POST["token"]
        if browser is not None and token != "":
            if browser == "Chrome":
                status = Device.add_device("FCM", token, request.user)
                return HttpResponse(status=status)

            """
            The commented lines below is the implementation for Safari browser
            Apples APNS certificat would be needed, cost ~1000 NOK/year
            The code has not been testet so no garanties it would work
            """
            # elif browser == "Safari":
            #     status = Device.add_device("APNS", token, request.user)
            #     return HttpResponse(status=status)
    else:
        return redirect(reverse("frontpage:home"))


@csrf_exempt
def send_notification(request):
    """Send notification to all users from notification/send url"""
    if request.method == "POST":
        payload_bytes = request.body
        payload_bytes_decoded = payload_bytes.decode("utf8")
        payload_json = json.loads(payload_bytes_decoded)
        serializer = CoffeeSubmissionSerializer(data=payload_json)

        is_authorized = serializer.is_authorized(
            payload_json["notification_key"], payload_json["topic"]
        )

        if is_authorized:
            topic = payload_json["topic"]

            if topic == "coffee":
                if CoffeeSubmission.fifteen_minutes_has_passed():
                    serializer.save()
                    subscriptions = Subscription.objects.filter(
                        subscription_type=1
                    )
                    subscribers = [sub.owner for sub in subscriptions]

                    CoffeeSubmission.send_coffee_notification(subscribers)
                    return JsonResponse(serializer.errors, status=201)
                else:
                    return JsonResponse(serializer.errors, status=402)
            else:
                return JsonResponse(serializer.errors, status=401)

        return JsonResponse(serializer.errors, status=401)
    else:
        return redirect(reverse("frontpage:home"))


class CoffeeLatestSubmission(generics.ListCreateAPIView):
    serializer_class = CoffeeSubmissionSerializer

    def get_queryset(self):
        queryset = CoffeeSubmission.objects.order_by("-id")
        if queryset.exists():
            return queryset[:1]
        else:
            return queryset
