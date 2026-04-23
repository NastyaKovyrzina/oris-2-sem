from django.urls import path
from . import views

urlpatterns = [
    path('', views.theory_list),
    path('theory/<int:pk>/edit/', views.TheoryUpdateView.as_view(), name='theory_update'),
    path('theory/<int:pk>/delete/', views.TheoryDeleteView.as_view(), name='theory_delete'),
]