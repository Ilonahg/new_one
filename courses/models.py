from django.db import models
from django.conf import settings


class SomeModel(models.Model):
    """
    Минимальная модель под ДЗ.
    Привязана к кастомному пользователю через settings.AUTH_USER_MODEL.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="some_models",
        verbose_name="Пользователь",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    condition_field = models.BooleanField(default=False, verbose_name="Условие выполнено")

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user} / {self.pk}"
