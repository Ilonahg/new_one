from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Course, Payment, Subscription
from .services import create_stripe_session
from .serializers import PaymentSerializer, SubscribeSerializer   # 👈 добавили
from django.http import HttpResponse

class SubscriptionView(APIView):
    """
    ✅ POST /subscribe/ – подписка или отписка пользователя от курса.
    Если подписки нет – создаём. Если есть – удаляем.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer   # 👈 добавили

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data["course_id"]

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


class PaymentView(APIView):
    """
    ✅ POST /pay/ – создаёт Stripe-сессию оплаты и возвращает ссылку.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer   # 👈 добавили

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data["course_id"]

        course = get_object_or_404(Course, id=course_id)

        # Создаём Stripe-сессию
        session = create_stripe_session(course)

        # Сохраняем платёж в базе
        Payment.objects.create(
            course=course,
            user=request.user,
            session_id=session.id,
            link=session.url,
            amount=course.price
        )

        return Response({"payment_url": session.url})

def payment_success(request):
    return HttpResponse("✅ Оплата прошла успешно!")

def payment_cancel(request):
    return HttpResponse("❌ Оплата была отменена.")