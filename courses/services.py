import stripe
from django.conf import settings
from django.core.mail import send_mail
from .models import Subscription

# 🔑 Настраиваем Stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)


def create_stripe_session(course):
    """
    Создание Stripe Checkout-сессии для оплаты курса.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # или 'rub'
                'product_data': {'name': course.title},
                'unit_amount': int(course.price * 100),  # цена в центах
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=settings.DOMAIN_NAME + '/success/',
        cancel_url=settings.DOMAIN_NAME + '/cancel/',
    )
    return session


def notify_course_subscribers(course):
    """
    Отправка писем всем подписчикам курса.
    """
    subscribers = Subscription.objects.filter(course=course).select_related("user")

    for sub in subscribers:
        user = sub.user
        if not user.email:
            continue

        subject = f"Обновление курса: {course.title}"
        message = (
            f"Здравствуйте, {user.first_name or 'пользователь'}!\n\n"
            f"Курс «{course.title}» был обновлён.\n"
            f"Зайдите на сайт, чтобы ознакомиться с новыми материалами.\n\n"
            f"С уважением, команда обучения."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
