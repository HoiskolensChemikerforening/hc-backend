from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.shortcuts import render
from .models import CGP
from .forms import CGPForm
@permission_required("elections.add_election")
@login_required
def cgp_admin(request):
    cgps = CGP.objects.all()

    if request.method == "POST":  # brukeren trykker på knappen
        CGP.create_new_cgp()


    context = {
        "cgps": cgps,
    }
    return render(request, "cgp/admin/admin.html", context)

@permission_required("elections.add_election")
@login_required
def cgp_edit(request, id):
    return render(request, "index.html")