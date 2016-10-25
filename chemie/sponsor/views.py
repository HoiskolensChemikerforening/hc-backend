from django.shortcuts import render
from .models import Sponsor

def show_sponsors(request):
    temp_sponsors = Sponsor.objects.all()

    sponsors = []
    for sponsor in temp_sponsors:
        #Assuming it was meant temp_sponsors in loop, not sponsors, since looping over an empty list makes no sense.
        if not sponsor.is_expired():
            sponsors.append(sponsor)

    return render(request, 'chemie/base.html', context={'sponsors': sponsors})
