from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")), # web app endpoint

    path("api-auth/", include("rest_framework.urls")), # for login/logout in the browsable API

    # API endpoints
    path("api/v1/", include("api.urls")), # API endpoint for students
]
