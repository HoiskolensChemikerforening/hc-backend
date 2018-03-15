from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Count, Q


def make_all_access_cards_unique(app, schema_editor):
    try:
        Profile = app.get_model('customprofile', 'Profile')
    except LookupError:
        print("Old model is no longer installed")
        return

    # Find all duplicate access card values
    duplicate_values = Profile.objects\
        .values('access_card')\
        .annotate(Count('id'))\
        .order_by()\
        .filter(id__count__gt=1)

    # Generate OR filter query based on these values
    q_duplicate_or = Q(access_card='This string itself excludes all profiles. Will match every profile if left empty.')
    for duplicate in duplicate_values:
        duplicate = duplicate.get('access_card')
        q_duplicate_or = q_duplicate_or | Q(access_card=duplicate)

        # Finally: Set access_card to empty string and saving the object
        # Model save function is called and will create a unique, and invalid (!), access card number
    duplicates = Profile.objects.filter(q_duplicate_or)

    for duplicate in duplicates:
        duplicate.access_card = f'{duplicate.pk} - INVALID'
        duplicate.save()


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(make_all_access_cards_unique, migrations.RunPython.noop),
    ]
    dependencies = [
        ('customprofile', '0001_initial'),
    ]
