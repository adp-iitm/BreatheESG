from django.urls import path

from apps.ingestion.views import DashboardView, DataSourceListView, UploadView

urlpatterns = [
    path("upload/", UploadView.as_view(), name="upload"),
    path("datasources/", DataSourceListView.as_view(), name="datasource-list"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
