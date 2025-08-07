from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription

@shared_task
def send_course_update_email(course_id):
    """Отправляет письма всем подписчикам курса"""
    course = Course.objects.get(id=course_id)
    subs = Subscription.objects.filter(course=course)

    for sub in subs:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлён. Зайдите, чтобы посмотреть новые материалы.',
            from_email='noreply@edu.com',
            recipient_list=[sub.user.email],
        )
    return f"Emails sent to {subs.count()} subscribers."
