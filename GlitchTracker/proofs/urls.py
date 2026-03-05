from django.urls import path
from . import views

urlpatterns = [
    path('', views.proof_list),
]