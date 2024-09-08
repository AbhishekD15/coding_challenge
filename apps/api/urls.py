from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "api"

urlpatterns = [
    # Course Endpoints
    path("admission/courses/", views.ListCourses.as_view(), name="list_courses"),
    path("admission/courses/create/", views.CreateCourse.as_view(), name="create_course"),
    path("admission/courses/<int:course_id>/", views.RetrieveCourse.as_view(), name="retrieve_course"),
    path("admission/courses/<int:course_id>/update/", views.UpdateCourse.as_view(), name="update_course"),
    path("admission/courses/<int:course_id>/delete/", views.DeleteCourse.as_view(), name="delete_course"),

    # Intake Endpoints (nested under Courses)
    path("admission/courses/<int:course_id>/intakes/", views.ListIntakes.as_view(), name="list_intakes"),
    path("admission/courses/<int:course_id>/intakes/create/", views.CreateIntake.as_view(), name="create_intake"),
    path("admission/courses/<int:course_id>/intakes/<int:intake_id>/", views.RetrieveIntake.as_view(), name="retrieve_intake"),
    path("admission/courses/<int:course_id>/intakes/<int:intake_id>/update/", views.UpdateIntake.as_view(), name="update_intake"),
    path("admission/courses/<int:course_id>/intakes/<int:intake_id>/delete/", views.DeleteIntake.as_view(), name="delete_intake"),

    # JWT Authentication Endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Health Check Endpoint
    path('health/', views.HealthCheck.as_view(), name='health_check'),
]
