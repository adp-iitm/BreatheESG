from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    class SourceType(models.TextChoices):
        SAP = "SAP", "SAP"
        UTILITY = "UTILITY", "UTILITY"
        TRAVEL = "TRAVEL", "TRAVEL"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="datasources")
    source_type = models.CharField(max_length=20, choices=SourceType.choices)
    ingestion_method = models.CharField(max_length=50, default="CSV_UPLOAD")
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=150, default="analyst@example.com")


class RawRecord(models.Model):
    class ProcessingStatus(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        NORMALIZED = "NORMALIZED", "NORMALIZED"
        FAILED = "FAILED", "FAILED"

    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="raw_records")
    row_number = models.PositiveIntegerField()
    raw_json = models.JSONField()
    processing_status = models.CharField(
        max_length=20, choices=ProcessingStatus.choices, default=ProcessingStatus.PENDING
    )
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("datasource", "row_number")
