from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.ingestion.urls")),
    path("api/", include("apps.normalization.urls")),
    path("api/", include("apps.review.urls")),
]
