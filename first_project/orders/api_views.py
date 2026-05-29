from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(summary="Список заказов (только для авторизованных)", tags=["Заказы"]),
    post=extend_schema(summary="Создать заказ", tags=["Заказы"])
)
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свои заказы
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(summary="Детали заказа", tags=["Заказы"]),
    put=extend_schema(summary="Обновить заказ (только статус, например)", tags=["Заказы"]),
    patch=extend_schema(summary="Частично обновить заказ", tags=["Заказы"]),
    delete=extend_schema(summary="Удалить заказ (только если не оплачен)", tags=["Заказы"])
)
class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)