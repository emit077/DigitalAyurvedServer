from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BlogData

User = get_user_model()


class BlogDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogData
        fields = ['blog_data', 'created', 'modified']
