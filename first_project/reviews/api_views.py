from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(summary="Список отзывов", tags=["Отзывы"]),
    post=extend_schema(summary="Создать отзыв", tags=["Отзывы"])
)
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(summary="Детали отзыва", tags=["Отзывы"]),
    put=extend_schema(summary="Обновить отзыв", tags=["Отзывы"]),
    patch=extend_schema(summary="Частично обновить отзыв", tags=["Отзывы"]),
    delete=extend_schema(summary="Удалить отзыв", tags=["Отзывы"])
)
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]