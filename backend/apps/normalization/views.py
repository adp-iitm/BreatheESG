from rest_framework import generics

from apps.normalization.models import NormalizedActivity
from apps.normalization.serializers import NormalizedActivitySerializer


class ActivityListView(generics.ListAPIView):
    serializer_class = NormalizedActivitySerializer

    def get_queryset(self):
        queryset = NormalizedActivity.objects.select_related("raw_record", "raw_record__datasource").order_by("-created_at")
        source_type = self.request.query_params.get("source_type")
        scope = self.request.query_params.get("scope")
        review_status = self.request.query_params.get("review_status")
        if source_type:
            queryset = queryset.filter(raw_record__datasource__source_type=source_type)
        if scope:
            queryset = queryset.filter(scope=scope)
        if review_status:
            queryset = queryset.filter(review_status=review_status)
        return queryset
