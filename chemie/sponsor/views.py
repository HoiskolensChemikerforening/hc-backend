from django.shortcuts import render
from .models import sponsor

def show_sponsors(request):
    temp_sponsors = sponsor.objects.all()

    sponsors = []
    for sponsor in sponsors:
        if not sponsor.is_expired():
            sponsors.append(sponsor)

    return render(request, 'chemie/base.html', context={'sponsors': sponsors})
