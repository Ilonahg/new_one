from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('api-auth/', include('rest_framework.urls')),   # для кнопки Log in
]
