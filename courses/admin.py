from django.contrib import admin
from .models import SomeModel


@admin.register(SomeModel)
class SomeModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "condition_field", "created_at")
    list_filter = ("condition_field", "created_at")
    search_fields = ("user__username",)
