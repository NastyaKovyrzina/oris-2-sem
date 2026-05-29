from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Theory
from .serializers import TheorySerializer

@extend_schema_view(
    get=extend_schema(summary="Список теорий", tags=["Теории"]),
    post=extend_schema(summary="Создать теорию", tags=["Теории"]),
)
class TheoryListCreateView(generics.ListCreateAPIView):
    queryset = Theory.objects.all()
    serializer_class = TheorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@extend_schema_view(
    get=extend_schema(summary="Детали теории", tags=["Теории"]),
    put=extend_schema(summary="Полное обновление теории", tags=["Теории"]),
    patch=extend_schema(summary="Частичное обновление теории", tags=["Теории"]),
    delete=extend_schema(summary="Удалить теорию", tags=["Теории"]),
)
class TheoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theory.objects.all()
    serializer_class = TheorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете редактировать чужую теорию.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете удалить чужую теорию.")
        instance.delete()