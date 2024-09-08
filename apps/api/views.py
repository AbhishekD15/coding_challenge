from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.http import Http404
from apps.admission.models import Course, Intake
from .serializers import CourseSerializer, IntakeSerializer

# HealthCheck View
class HealthCheck(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"}, status=status.HTTP_200_OK)


# Custom Pagination Class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Course Views
class ListCourses(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        try:
            with_intakes = request.query_params.get('with_intakes', 'false').lower() == 'true'

            if with_intakes:
                courses = Course.objects.prefetch_related('intakes').order_by('id').all()
            else:
                courses = Course.objects.order_by('id').all()

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(courses, request)
            if with_intakes:
                serializer = CourseSerializer(page, many=True)
            else:
                serializer = CourseSerializer(page, many=True, exclude_intakes=True)

            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCourse(APIView):
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
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.view_course'):
                return Response({"detail": "You do not have permission to view this course."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCourse(APIView):
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
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteCourse(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.delete_course'):
                return Response({"detail": "You do not have permission to delete this course."}, status=status.HTTP_403_FORBIDDEN)
            
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Intake Views

class ListIntakes(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            if not request.user.has_perm('admission.view_intake'):
                return Response({"detail": "You do not have permission to view these intakes."}, status=status.HTTP_403_FORBIDDEN)
            
            intakes = course.intakes.order_by('id').all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(intakes, request)
            serializer = IntakeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateIntake(APIView):
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
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, intake_id, *args, **kwargs):
        try:
            intake = get_object_or_404(Intake, course__id=course_id, id=intake_id)
            if not request.user.has_perm('admission.view_intake'):
                return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = IntakeSerializer(intake)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateIntake(APIView):
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
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteIntake(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id, intake_id, *args, **kwargs):
        try:
            intake = get_object_or_404(Intake, course__id=course_id, id=intake_id)
            if not request.user.has_perm('admission.delete_intake'):
                return Response({"detail": "You do not have permission to delete this intake."}, status=status.HTTP_403_FORBIDDEN)
            
            intake.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)