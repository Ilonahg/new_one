from django.urls import path
from .views import create_somemodel

urlpatterns = [
    path("create/", create_somemodel, name="create_somemodel"),
]
