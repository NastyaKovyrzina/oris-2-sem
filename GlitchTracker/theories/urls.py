from django.urls import path
from . import views

urlpatterns = [
    path('', views.theory_list),
]