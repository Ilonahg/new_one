from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """
    Модель курса.
    """
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")  # из materials
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Цена")
    owner = models.ForeignKey(  # из materials
        User,
        on_delete=models.CASCADE,
        related_name='owned_courses',
        null=True,
        blank=True,
        verbose_name="Автор курса"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # нужно для проверки 4 часов

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """
    Модель урока (материала курса).
    """
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")  # из materials
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(  # из materials
        User,
        on_delete=models.CASCADE,
        related_name='owned_lessons',
        null=True,
        blank=True,
        verbose_name="Автор урока"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # тоже пригодится

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """
    Подписка пользователя на курс.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"


class Payment(models.Model):
    """
    Платёж за курс (Stripe).
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session_id = models.CharField(max_length=500, verbose_name="ID сессии Stripe")
    link = models.URLField(max_length=1000, verbose_name="Ссылка на оплату")
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user} – {self.course} – {self.amount}$"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
