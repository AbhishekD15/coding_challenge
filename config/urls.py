from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('apps.api.urls')),  # Add this line to include the API URLs
]
