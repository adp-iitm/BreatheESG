from django.urls import path

from apps.review.views import ApproveActivityView, RejectActivityView

urlpatterns = [
    path("activities/<int:pk>/approve/", ApproveActivityView.as_view(), name="activity-approve"),
    path("activities/<int:pk>/reject/", RejectActivityView.as_view(), name="activity-reject"),
]
