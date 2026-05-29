from django.urls import path
from .views import order_list
from . import api_views
from . import views

app_name = 'orders'

urlpatterns = [
    path('list/', views.order_list, name='order_list'),
    path('api/orders/', api_views.OrderListCreateView.as_view(), name="api_orders"),
    path('api/orders/<int:pk>/', api_views.OrderRetrieveUpdateDestroyView.as_view(), name="api_order_detail"),
]