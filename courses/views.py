from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer
from .services import create_stripe_session  # используется в оплате
from .tasks import send_course_update_email_task  # celery-задача на рассылку


# ✅ Список всех курсов
class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Детали одного курса
class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Создание курса
class CourseCreateView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Обновление курса (рассылка уведомлений через Celery)
class CourseUpdateView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        После обновления курса:
        - сохраняем изменения
        - запускаем celery-задачу на отправку писем подписчикам
        """
        course = serializer.save()

        # 🕓 (дополнительно) если нужно — не рассылать, если обновлялся <4 часов назад
        if course.updated_at and timezone.now() - course.updated_at < timedelta(hours=4):
            return

        # 🚀 Асинхронный запуск задачи Celery
        send_course_update_email_task.delay(course.id)


# ✅ Удаление курса
class CourseDeleteView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Список всех уроков
class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


# ✅ Создание урока
class LessonCreateView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


# ✅ Подписка / отписка на курс
class SubscriptionView(APIView):
    """
    POST-запрос с course_id:
      - если пользователь не подписан → создаём подписку
      - если уже подписан → отписываем
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )

        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message})


# ✅ Оплата курса (Stripe)
class PaymentView(APIView):
    """
    POST-запрос с course_id:
    - создаёт Stripe-сессию
    - сохраняет платёж в БД
    - возвращает ссылку на оплату
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Создаём Stripe-сессию через сервисную функцию
        session = create_stripe_session(course)

        # Сохраняем платёж
        payment = Payment.objects.create(
            course=course,
            user=request.user,
            session_id=session.id,
            link=session.url,
            amount=course.price
        )

        return Response({"payment_url": session.url})
