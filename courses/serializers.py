from rest_framework import serializers
from .models import Course, Lesson   # ✅ импортируем модели


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']
        read_only_fields = ['owner']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'owner']
        read_only_fields = ['owner']
