# courses/tests.py
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Subscription

User = get_user_model()

class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Django Basics")

    def test_course_list(self):
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Django Basics", str(response.data))

    def test_subscription(self):
        response = self.client.post("/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Подписка добавлена")

        # повторный вызов должен удалить подписку
        response = self.client.post("/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.data["message"], "Подписка удалена")
