from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer
from .services import create_stripe_session
from .tasks import send_course_update_email


# ✅ Список всех курсов
class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Детали курса
class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Создание курса
class CourseCreateView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Обновление курса (и отправка уведомлений)
class CourseUpdateView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        course = serializer.save()
        # 🚀 Асинхронно отправляем письма подписчикам
        send_course_update_email.delay(course.id)


# ✅ Удаление курса
class CourseDeleteView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ✅ Список уроков
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Создаём Stripe-сессию
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
