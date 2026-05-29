from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Anomaly
from .serializers import AnomalySerializer

@extend_schema_view(
    get=extend_schema(summary="Список аномалий", tags=["Аномалии"]),
    post=extend_schema(summary="Создать аномалию", tags=["Аномалии"]),
)
class AnomalyListCreateView(generics.ListCreateAPIView):
    queryset = Anomaly.objects.all()
    serializer_class = AnomalySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@extend_schema_view(
    get=extend_schema(summary="Детали аномалии", tags=["Аномалии"]),
    put=extend_schema(summary="Полное обновление аномалии", tags=["Аномалии"]),
    patch=extend_schema(summary="Частичное обновление аномалии", tags=["Аномалии"]),
    delete=extend_schema(summary="Удалить аномалию", tags=["Аномалии"]),
)
class AnomalyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anomaly.objects.all()
    serializer_class = AnomalySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете редактировать чужую аномалию.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете удалить чужую аномалию.")
        instance.delete()