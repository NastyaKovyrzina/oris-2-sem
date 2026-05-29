from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(summary="Получить свой профиль", tags=["Пользователи"]),
    put=extend_schema(summary="Обновить профиль целиком", tags=["Пользователи"]),
    patch=extend_schema(summary="Частично обновить профиль", tags=["Пользователи"])
)
class MyProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

@extend_schema(
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя и его профиль",
    tags=["Пользователи"]
)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]