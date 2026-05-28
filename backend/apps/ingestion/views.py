from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.models import Company, DataSource, RawRecord
from apps.ingestion.serializers import DataSourceSerializer
from apps.ingestion.services import ingest_csv_and_normalize
from apps.normalization.models import NormalizedActivity


class UploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get("file")
        source_type = request.data.get("source_type")
        company_id = request.data.get("company_id")
        uploaded_by = request.data.get("uploaded_by", "analyst@example.com")
        if not file_obj or not source_type or not company_id:
            return Response({"detail": "file, source_type and company_id are required"}, status=400)
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"detail": "company_id is invalid"}, status=400)

        try:
            datasource = ingest_csv_and_normalize(
                company=company, source_type=source_type, uploaded_by=uploaded_by, uploaded_file=file_obj
            )
            return Response(DataSourceSerializer(datasource).data, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)


class DataSourceListView(generics.ListAPIView):
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.select_related("company").order_by("-uploaded_at")


class DashboardView(APIView):
    def get(self, request):
        totals = RawRecord.objects.aggregate(
            total_rows=Count("id"),
            failed_rows=Count("id", filter=Q(processing_status=RawRecord.ProcessingStatus.FAILED)),
        )
        review = NormalizedActivity.objects.aggregate(
            flagged_rows=Count("id", filter=Q(review_status=NormalizedActivity.ReviewStatus.FLAGGED)),
            approved_rows=Count("id", filter=Q(review_status=NormalizedActivity.ReviewStatus.APPROVED)),
        )
        return Response({**totals, **review})
