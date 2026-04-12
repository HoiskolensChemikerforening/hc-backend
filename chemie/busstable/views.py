from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import permission_required

@permission_required("buss.see_all")
def index(request):
    if request.user.username == "tabletshop":
        return render(request, "buss.html")
    else:
        return render(request, "buss.html")
        #raise Http404("Page not found")