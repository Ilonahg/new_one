from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True)
def send_notification_task(self, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    if user.email:
        send_mail(
            "Объект создан",
            "Ваш объект успешно создан.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    return "ok"
