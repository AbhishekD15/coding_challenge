from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.admission.models import Course
from .serializers import CourseSerializer

class ListCourses(APIView):
    """
    View to list all courses along with their intakes.
    """
    def get(self, request, *args, **kwargs):
        # Query all courses
        courses = Course.objects.prefetch_related('intakes').all()
        # Serialize the courses with the related intakes
        serializer = CourseSerializer(courses, many=True)
        # Return the data as JSON
        return Response(serializer.data)

class HealthCheck(APIView):
    """
    A simple health check endpoint to verify if the API is up and running.
    """
    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"}, status=status.HTTP_200_OK)

