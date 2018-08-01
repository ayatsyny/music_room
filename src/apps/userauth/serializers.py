from rest_framework import serializers
from .models import Review, Course


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwarg = {
            'email': {'write_only': True}
        }
        fields = (
            'id',
            'course',
            'name',
            'email',
            'review',
            'rating',
            'create_at'
        )
        model = Review


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'url'
        )
        model = Course
