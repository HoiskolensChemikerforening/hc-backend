from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_socialeventregistration_registration_group_members"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bedpres",
            name="allowed_groups",
        ),
        migrations.RemoveField(
            model_name="social",
            name="allowed_groups",
        ),
        migrations.RemoveField(
            model_name="socialeventregistration",
            name="registration_group_members",
        ),
        migrations.DeleteModel(
            name="BaseRegistrationGroup",
        ),
    ]
