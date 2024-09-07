from rest_framework.views import APIView
from rest_framework.response import Response
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
