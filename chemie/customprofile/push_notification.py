from push_notifications.models import APNSDevice, GCMDevice

HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"


def save_device(token, browser, user):
    if browser == "Safari":
        if APNSDevice.objects.filter(registration_id=token).count() == 0:
            APNSDevice.objects.create(registration_id=token,cloud_message_type="FCM", user=user)
    else:
        if GCMDevice.objects.filter(registration_id=token).count() == 0:
            GCMDevice.objects.create(registration_id=token,cloud_message_type="FCM", user=user)




def APNS_send(message, title, icon=HC_ICON):
    devices = APNSDevice.objects.all()
    devices.send_message(message,
                         extra={
                             "title": title,
                             "icon": icon,
                         })


def GCM_send(message, title,icon=HC_ICON):
    devices = GCMDevice.objects.all()
    devices.send_message(message,
                         extra={
                             "title": title,
                             "icon": icon,
                         })


def send(message, title,icon=HC_ICON):
    GCM_send(message, title,icon)
    APNS_send(message,title,icon)

