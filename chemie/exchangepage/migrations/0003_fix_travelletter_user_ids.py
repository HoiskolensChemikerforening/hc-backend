from django.db import migrations

def convert_profile_ids_to_user_ids(apps, schema_editor):
    Travelletter = apps.get_model("exchangepage", "Travelletter")
    Profile = apps.get_model("customprofile", "Profile")

    for tl in Travelletter.objects.all():
        if tl.user_id is None:
            continue

        try:
            profile = Profile.objects.get(id=tl.user_id)
            tl.user_id = profile.user_id  # convert Profile.id → User.id
            tl.save(update_fields=["user_id"])
        except Profile.DoesNotExist:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('exchangepage', '0002_auto_20260412_1147'),
        ('customprofile', '0025_auto_20260122_1837'),
    ]

    operations = [
        migrations.RunPython(convert_profile_ids_to_user_ids),
    ]
