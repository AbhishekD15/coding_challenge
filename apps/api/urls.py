from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("admission/courses/", views.ListCourses.as_view(), name="list_courses"),
    path("health/", views.HealthCheck.as_view(), name="health_check"),
]
