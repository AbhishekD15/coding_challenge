from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.admission.models import Course, Intake
from .serializers import CourseSerializer, IntakeSerializer

# HealthCheck View
class HealthCheck(APIView):
    """
    A simple health check endpoint to verify if the API is up and running.
    This endpoint is public and does not require authentication.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"}, status=status.HTTP_200_OK)


# Course Views
class ListCourses(APIView):
    """
    View to list all courses.
    Allows optional inclusion of intakes via a query parameter `?with_intakes=true`.
    Only authenticated users can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Check if the query parameter 'with_intakes' is passed and equals 'true'
            with_intakes = request.query_params.get('with_intakes', 'false').lower() == 'true'

            if with_intakes:
                courses = Course.objects.prefetch_related('intakes').all()  # Prefetch intakes for optimization
                serializer = CourseSerializer(courses, many=True)
            else:
                courses = Course.objects.all()  # No need to prefetch intakes
                serializer = CourseSerializer(courses, many=True, exclude_intakes=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCourse(APIView):
    """
    View to create a new course.
    Only users with 'add_course' permission can create a new course.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('admission.add_course'):
            return Response({"detail": "You do not have permission to create a course."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCourse(APIView):
    """
    View to retrieve a single course by ID.
    Only users with 'view_course' permission can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.view_course'):
                return Response({"detail": "You do not have permission to view this course."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCourse(APIView):
    """
    View to update a course by ID.
    Only users with 'change_course' permission can update a course.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.change_course'):
                return Response({"detail": "You do not have permission to update this course."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteCourse(APIView):
    """
    View to delete a course by ID.
    Only users with 'delete_course' permission can delete a course.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.delete_course'):
                return Response({"detail": "You do not have permission to delete this course."}, status=status.HTTP_403_FORBIDDEN)
            
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Intake Views

class ListIntakes(APIView):
    """
    View to list all intakes for a specific course.
    Only users with 'view_intake' permission can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.view_intake'):
                return Response({"detail": "You do not have permission to view these intakes."}, status=status.HTTP_403_FORBIDDEN)
            
            intakes = course.intakes.all()
            serializer = IntakeSerializer(intakes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateIntake(APIView):
    """
    View to create an intake for a specific course.
    Only users with 'add_intake' permission can create an intake.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.add_intake'):
                return Response({"detail": "You do not have permission to create an intake."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = IntakeSerializer(data=request.data)
            if serializer.is_valid():
                intake = serializer.save(course=course)
                return Response(IntakeSerializer(intake).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveIntake(APIView):
    """
    View to retrieve a specific intake for a course.
    Only users with 'view_intake' permission can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, intake_id, *args, **kwargs):
        try:
            intake = get_object_or_404(Intake, course__id=course_id, id=intake_id)
            if not request.user.has_perm('admission.view_intake'):
                return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = IntakeSerializer(intake)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateIntake(APIView):
    """
    View to update a specific intake for a course.
    Only users with 'change_intake' permission can update an intake.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, course_id, intake_id, *args, **kwargs):
        try:
            intake = get_object_or_404(Intake, course__id=course_id, id=intake_id)
            if not request.user.has_perm('admission.change_intake'):
                return Response({"detail": "You do not have permission to update this intake."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = IntakeSerializer(intake, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteIntake(APIView):
    """
    View to delete a specific intake for a course.
    Only users with 'delete_intake' permission can delete an intake.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id, intake_id, *args, **kwargs):
        try:
            intake = get_object_or_404(Intake, course__id=course_id, id=intake_id)
            if not request.user.has_perm('admission.delete_intake'):
                return Response({"detail": "You do not have permission to delete this intake."}, status=status.HTTP_403_FORBIDDEN)
            
            intake.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
