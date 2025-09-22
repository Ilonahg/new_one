# courses/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Course, Subscription

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_course_update_email(self, course_id: int):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return

    subs = Subscription.objects.filter(course=course).select_related('user')
    recipients = [s.user.email for s in subs if s.user and s.user.email]

    if not recipients:
        return

    subject = f"Обновление курса: {course.title}"
    message = (
        f"Курс «{course.title}» был обновлён {timezone.now():%d.%m.%Y %H:%M}.\n"
        f"Описание: {course.description or 'без изменений.'}\n"
        f"Зайдите в кабинет, чтобы посмотреть детали."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
        recipient_list=recipients,
        fail_silently=False,
    )
