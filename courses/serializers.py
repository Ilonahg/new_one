from rest_framework import serializers
from .models import Lesson, Course, Subscription
from .validators import validate_youtube_link


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "lessons", "is_subscribed"]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


# ✅ Сериализатор для Stripe оплаты
class PaymentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(help_text="ID курса для оплаты")


# ✅ Сериализатор для подписки на курс
class SubscribeSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(help_text="ID курса для подписки")
