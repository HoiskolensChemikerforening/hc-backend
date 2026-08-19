from django.db import migrations

def convert_profile_ids_to_user_ids(apps, schema_editor):
    Travelletter = apps.get_model("exchangepage", "Travelletter")
    Profile = apps.get_model("customprofile", "Profile")

    # Only process rows where the profile exists
    valid_profiles = Profile.objects.values_list("id", "user_id")

    profile_map = {pid: uid for pid, uid in valid_profiles}

    for tl in Travelletter.objects.all():
        old_id = tl.user_id

        # Skip if no profile exists for this ID
        if old_id not in profile_map:
            continue

        # Update to the correct user_id
        tl.user_id = profile_map[old_id]
        tl.save(update_fields=["user_id"])
        
class Migration(migrations.Migration):

    dependencies = [
        ('exchangepage', '0002_auto_20260412_1147'),
        ('customprofile', '0025_auto_20260122_1837'),
    ]

    operations = [
        migrations.RunPython(convert_profile_ids_to_user_ids),
    ]
