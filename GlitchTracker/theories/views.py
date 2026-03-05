from django.shortcuts import render
from .models import Theory

def theory_list(request):
    theories = Theory.objects.all()

    return render(request, "theories/list.html", {
        "theories": theories
    })