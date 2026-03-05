from django.shortcuts import render
from .models import Anomaly

def index(request):
    return render(request, 'anomalies/home.html')


def anomaly_list(request):
    anomalies = Anomaly.objects.all()
    return render(request, 'anomalies/list.html', {
        'anomalies': anomalies
    })