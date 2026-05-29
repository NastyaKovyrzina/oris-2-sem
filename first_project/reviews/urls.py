from django.urls import path
from . import views
from . import api_views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('api/reviews/', api_views.ReviewListCreateView.as_view(), name="api_reviews"),
    path('api/reviews/<int:pk>/', api_views.ReviewRetrieveUpdateDestroyView.as_view(), name="api_review_detail"),
]