from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import Pictureform
from .models import Submission


@login_required
def post_pic(request):
    form = Pictureform(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(request, messages.SUCCESS,
                             'Bilde har blitt sendt inn!',
                             extra_tags='Bilde ble sendt')
        return redirect(reverse('carousel:view'))
    context = {
        "form": form,
    }

    return render(request, "picturecarousel/post_pic.html", context)


def view_carousel(request):
    pictures = Submission.objects.filter(approved=True)
    context = {
    "pictures": pictures
    }
    return render(request, "picturecarousel/carousel.html", context)


def view_pic_approve(request):
    pictures = Submission.objects.all()
    context = {
    "pictures": pictures
    }
    return render(request, "picturecarousel/approve.html", context)


def approve(request, picture_id):
    if request.method == 'POST':
        pic = get_object_or_404(Submission, id=picture_id)
        if 'approve' in request.POST:
            pic.approve()
            pic.save()
            messages.add_message(request, messages.SUCCESS, 'Bildet er godkjent!', extra_tags="Suksess!")
            return HttpResponseRedirect(reverse('carousel:approve'))
        if 'delete' in request.POST:
            pic.delete()
            messages.add_message(request, messages.SUCCESS, 'Bildet er slettet.')
            return HttpResponseRedirect(reverse('carousel:approve'))
    return render(request, 'picturecarousel/approve.html')
