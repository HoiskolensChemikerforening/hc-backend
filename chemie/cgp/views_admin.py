from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.shortcuts import render
from .models import CGP

@permission_required("elections.add_election")
@login_required
def admin_start_cgp(request):
    if request.method == "POST":  # brukeren trykker på knappen
        CGP.create_new_election()
        return redirect("")

    return render(request, "index.html")

@permission_required("elections.add_election")
@login_required
def create_country(request):
    return render(request, "index.html")