from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # можно добавить доп. поля, если надо
    # phone = models.CharField(max_length=20, blank=True, null=True)
    pass
