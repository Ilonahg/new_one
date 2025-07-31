# courses/validators.py
from rest_framework import serializers

def validate_youtube_link(value):
    if "youtube.com" not in value:
        raise serializers.ValidationError("Можно добавлять только ссылки на YouTube!")
    return value
