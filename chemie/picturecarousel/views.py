from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import Pictureform
from .models import Contribution


@login_required
def submit_picture(request):
    form = Pictureform(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(request, messages.SUCCESS,
                             'Bildet har blitt sendt inn!',
                             extra_tags='Bildet ble sendt')
        return redirect(reverse('carousel:submit'))
    context = {
        "form": form,
    }

    return render(request, "picturecarousel/submit_picture.html", context)


def view_carousel(request):
    pictures = Contribution.objects.get_all_shuffled()
    context = {
    "pictures": pictures
    }
    return render(request, "picturecarousel/carousel.html", context)


def approve_pictures(request):
    awaiting_approval = Contribution.objects.filter(approved=False)
    approved = Contribution.objects.filter(approved=True)
    context = {
    "awaiting_approval": awaiting_approval,
    "approved": approved,
    }
    return render(request, "picturecarousel/approve.html", context)


def approve_deny(request, picture_id, deny=False):
    if request.method == 'POST':
        picture = get_object_or_404(Contribution, id=picture_id)
        if not deny:
            picture.approve()
            picture.save()
            messages.add_message(request, messages.SUCCESS, 'Bildet er godkjent', extra_tags="Yay!")
        else:
            picture.delete()
            messages.add_message(request, messages.SUCCESS, 'Bildet ble slettet', extra_tags='Slettet!')
        return HttpResponseRedirect(reverse('carousel:overview'))
    return HttpResponseRedirect(reverse('carousel:overview'))