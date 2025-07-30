from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # 🔒 Модераторы не могут создавать курсы
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модератор не может создавать курсы.")
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # 🔒 Модераторы не могут удалять курсы
        if request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модератор не может удалять курсы.")
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        """
        Права доступа:
        - update/partial_update → владелец или модератор
        - все остальные → авторизованные пользователи
        """
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        return [IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        # 🔒 Модераторы не могут создавать уроки
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модератор не может создавать уроки.")
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # 🔒 Модераторы не могут удалять уроки
        if request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модератор не может удалять уроки.")
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        """
        Права доступа:
        - update/partial_update → владелец или модератор
        - все остальные → авторизованные пользователи
        """
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        return [IsAuthenticated()]
