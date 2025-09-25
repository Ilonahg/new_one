from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Минимальная кастомная модель пользователя.
    Можно добавлять свои поля при необходимости.
    """
    pass
