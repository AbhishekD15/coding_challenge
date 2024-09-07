from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "api"

urlpatterns = [
    path("admission/courses/", views.ListCourses.as_view(), name="list_courses"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # JWT token obtain
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # JWT token refresh
]
