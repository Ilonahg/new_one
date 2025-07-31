# courses/urls.py
from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    LessonListView, LessonCreateView, SubscriptionView
)

urlpatterns = [
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view()),
    path('courses/create/', CourseCreateView.as_view()),
    path('courses/update/<int:pk>/', CourseUpdateView.as_view()),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view()),

    path('lessons/', LessonListView.as_view()),
    path('lessons/create/', LessonCreateView.as_view()),

    path('subscribe/', SubscriptionView.as_view()),  # POST {course_id: 1}
]
