from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    content = models.TextField(blank=True, null=True, verbose_name="Содержание урока")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Курс")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', verbose_name="Владелец")

    def __str__(self):
        return f"{self.title} (Курс: {self.course.title})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
