from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import Pictureform
from .models import Picture


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
        return redirect(reverse('frontpage:home'))
    context = {
        "form": form,
    }

    return render(request, "picturecarousel/post_pic.html", context)

def view_carousel(request):
    pictures = Picture.objects.all()
    context = {
    "pictures": pictures
    }
    return render(request, "picturecarousel/carousel.html", context)


def view_pic_approve(request):
    pictures = Picture.objects.all()
    context = {
    "pictures": pictures
    }
    return render(request, "picturecarousel/approve.html", context)


def approve(request, picture_id):
    if request.method == 'POST':
        pic = get_object_or_404(Picture, id=picture_id)
        if 'approve' in request.POST:
            pic.approved == 1
            messages.add_message(request, messages.SUCCESS, 'Bildet er godkjent!')
            return HttpResponseRedirect()
        if 'delete' in request.POST:
            pic.delete()
            messages.add_message(request, messages.SUCCESS, 'Bildet er slettet.')
            return HttpResponseRedirect()
    return render(request, 'picturecarousel/approve.html')
