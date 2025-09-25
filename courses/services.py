from .tasks import send_notification_task

def process_new_object(instance):
    """
    Сервисная функция — проверяет условие и запускает celery task.
    """
    if getattr(instance, "condition_field", False):
        # В eager-режиме выполнится сразу, без Redis/воркера
        send_notification_task.delay(instance.user_id)
