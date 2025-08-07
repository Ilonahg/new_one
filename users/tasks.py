from celery import shared_task
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def block_inactive_users():
    """Блокирует пользователей, которые не заходили больше 30 дней"""
    month_ago = now() - timedelta(days=30)
    users_to_block = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = users_to_block.update(is_active=False)
    return f"Blocked {count} users"
