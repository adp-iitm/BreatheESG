from rest_framework import serializers

from apps.normalization.models import NormalizedActivity


class NormalizedActivitySerializer(serializers.ModelSerializer):
    source_type = serializers.CharField(source="raw_record.datasource.source_type", read_only=True)
    raw_row = serializers.JSONField(source="raw_record.raw_json", read_only=True)

    class Meta:
        model = NormalizedActivity
        fields = [
            "id",
            "company",
            "raw_record",
            "source_type",
            "activity_type",
            "scope",
            "category",
            "activity_date",
            "quantity",
            "original_unit",
            "normalized_unit",
            "normalized_quantity",
            "emission_factor",
            "co2e_emissions",
            "review_status",
            "locked",
            "validation_issues",
            "raw_row",
            "created_at",
        ]
