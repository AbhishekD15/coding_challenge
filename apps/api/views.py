from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from apps.admission.models import Course
from .serializers import CourseSerializer

class ListCourses(APIView):
    """
    View to list all courses along with their intakes.
    Only users with 'view_course' permission can access this endpoint.
    """
    permission_classes = [DjangoModelPermissions]  # Check model-level permissions

    def get_queryset(self):
        return Course.objects.prefetch_related('intakes').all()

    def get(self, request, *args, **kwargs):
        courses = self.get_queryset()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class HealthCheck(APIView):
    """
    A simple health check endpoint to verify if the API is up and running.
    This endpoint is public and does not require authentication.
    """
    permission_classes = [AllowAny]  # This makes the endpoint public

    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"}, status=status.HTTP_200_OK)