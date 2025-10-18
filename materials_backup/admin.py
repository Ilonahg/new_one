from django.contrib import admin
from materials_backup.models import Course, Lesson

admin.site.register(Course)
admin.site.register(Lesson)
# НЕ Регистрируй здесь Payment — он уже зарегистрирован в users/admin.py
