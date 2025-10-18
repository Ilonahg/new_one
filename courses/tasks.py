from celery import shared_task
from .models import Course
from .services import notify_course_subscribers


@shared_task
def send_course_update_email_task(course_id):
    """
    Асинхронная задача — вызвать сервисную функцию отправки писем.
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return
    notify_course_subscribers(course)
