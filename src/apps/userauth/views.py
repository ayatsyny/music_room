from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers


class ListCourse(APIView):
    def get(self, request, format=None):
        courses = models.Course.objects.all()
        serializer = serializers.CourseSerializer(courses, many=True)
        return Response(serializer.data)
