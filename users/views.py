from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer   # ✅ добавили импорт

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':       # регистрация
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':       # доступ к регистрации открыт
            return [AllowAny()]
        return [IsAuthenticated()]
