from push_notifications.models import APNSDevice, GCMDevice


def save_device(token, browser, user):
    if browser == "Safari":
        pass #TODO APNSDevice
    else:
        if GCMDevice.objects.filter(registration_id=token).count() == 0:
            GCMDevice.objects.create(registration_id=token,cloud_message_type="FCM", user=user)



def APNS_send(message, title, icon):
    devices = APNSDevice.objects.all()
    devices.send_message(message,
                         extra={
                             "title": title,
                             # "icon": icon
                         })


def GCM_send(message, title, icon):
    devices = GCMDevice.objects.all()
    devices.send_message(message,
                         extra={
                             "title": title,
                             #"icon": icon
                         })


def send(message, title, icon):
    GCM_send(message, title, icon)
    APNS_send(message,title,icon)

