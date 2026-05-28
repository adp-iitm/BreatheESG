from rest_framework import serializers

from apps.ingestion.models import Company, DataSource, RawRecord


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "industry", "created_at"]


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = [
            "id",
            "company",
            "source_type",
            "ingestion_method",
            "original_filename",
            "uploaded_at",
            "uploaded_by",
        ]


class RawRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawRecord
        fields = ["id", "datasource", "row_number", "raw_json", "processing_status", "error_message", "created_at"]
