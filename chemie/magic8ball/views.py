from django.shortcuts import render
from .forms import EightBallForm
from .models import MagicAnswer
import random

def eight_ball_view(request):
    svar = None
    vibe = None
    form = EightBallForm()

    if request.method == 'POST':
        form = EightBallForm(request.POST)
        if form.is_valid():
            alle_svar = MagicAnswer.objects.all()
            if alle_svar.exists():
                svar_obj = random.choice(list(alle_svar))
                svar = svar_obj.tekst
                vibe = svar_obj.vibe
            else:
                svar = "Ingen svar til spøsmålet ditt desverre :/"

    return render(request, 'idk.html', {'form': form, 'svar': svar, 'vibe': vibe,})