from django.urls import path
from . import views
from .views import AnomalyDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.anomaly_list, name='anomaly_list'),
    path('anomaly/<int:pk>/', AnomalyDetailView.as_view(), name='anomaly_detail'),
    path('create/', views.create_anomaly, name='create_anomaly'),
    path('anomaly/<int:pk>/edit/', views.AnomalyUpdateView.as_view(), name='anomaly_update'),
    path('anomaly/<int:pk>/delete/', views.AnomalyDeleteView.as_view(), name='anomaly_delete'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/add/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    ]