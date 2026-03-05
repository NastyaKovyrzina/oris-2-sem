from django.shortcuts import render
from .models import Proof

def proof_list(request):
    proofs = Proof.objects.all()

    return render(request, "proofs/list.html", {
        "proofs": proofs
    })