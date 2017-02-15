from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import Postform


@login_required
def post_votes(request):
    form = Postform(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(request, messages.SUCCESS,
                             'Sladderet ble mottatt, tusen takk!',
                             extra_tags='Du sladret')
        return redirect(reverse('frontpage:home'))
    context = {
        "form": form,
    }

    return render(request, "shitbox/post_form.html", context)
