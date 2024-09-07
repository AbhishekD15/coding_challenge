from rest_framework.views import APIView

from .serializers import CourseSerializer


class ListCourses(APIView):
    serializer_class = CourseSerializer
