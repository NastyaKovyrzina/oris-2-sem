from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(summary="Список категорий", tags=["Категории"]),
    post=extend_schema(summary="Создать категорию", tags=["Категории"])
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema_view(
    get=extend_schema(summary="Детали категории", tags=["Категории"]),
    put=extend_schema(summary="Обновить категорию целиком", tags=["Категории"]),
    patch=extend_schema(summary="Частично обновить категорию", tags=["Категории"]),
    delete=extend_schema(summary="Удалить категорию", tags=["Категории"])
)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema_view(
    get=extend_schema(summary="Список товаров", tags=["Товары"]),
    post=extend_schema(summary="Создать товар", tags=["Товары"])
)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema_view(
    get=extend_schema(summary="Детали товара", tags=["Товары"]),
    put=extend_schema(summary="Обновить товар целиком", tags=["Товары"]),
    patch=extend_schema(summary="Частично обновить товар", tags=["Товары"]),
    delete=extend_schema(summary="Удалить товар", tags=["Товары"])
)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]