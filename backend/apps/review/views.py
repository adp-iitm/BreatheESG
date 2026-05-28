from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.normalization.models import NormalizedActivity


class ApproveActivityView(APIView):
    def post(self, request, pk):
        activity = NormalizedActivity.objects.get(pk=pk)
        if activity.locked:
            return Response({"detail": "activity already locked"}, status=status.HTTP_400_BAD_REQUEST)
        previous = {"review_status": activity.review_status, "locked": activity.locked}
        activity.review_status = NormalizedActivity.ReviewStatus.APPROVED
        activity.locked = True
        activity.save(update_fields=["review_status", "locked"])
        AuditLog.objects.create(
            activity=activity,
            action="APPROVE",
            previous_value=previous,
            new_value={"review_status": activity.review_status, "locked": activity.locked},
        )
        return Response({"detail": "approved"})


class RejectActivityView(APIView):
    def post(self, request, pk):
        activity = NormalizedActivity.objects.get(pk=pk)
        if activity.locked:
            return Response({"detail": "activity already locked"}, status=status.HTTP_400_BAD_REQUEST)
        previous = {"review_status": activity.review_status}
        activity.review_status = NormalizedActivity.ReviewStatus.REJECTED
        activity.save(update_fields=["review_status"])
        AuditLog.objects.create(
            activity=activity,
            action="REJECT",
            previous_value=previous,
            new_value={"review_status": activity.review_status},
        )
        return Response({"detail": "rejected"})
