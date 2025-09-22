# courses/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from .tasks import send_course_update_email

@receiver(post_save, sender=Course)
def course_updated(sender, instance: Course, created, **kwargs):
    if created:
        return  # на создание не шлём
    # отложить отправку на 5 минут (300 сек)
    send_course_update_email.apply_async(args=[instance.id], countdown=300)
