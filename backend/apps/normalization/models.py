from django.db import models

from apps.ingestion.models import Company, RawRecord


class NormalizedActivity(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        FLAGGED = "FLAGGED", "FLAGGED"
        APPROVED = "APPROVED", "APPROVED"
        REJECTED = "REJECTED", "REJECTED"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="activities")
    raw_record = models.OneToOneField(RawRecord, on_delete=models.PROTECT, related_name="activity")
    activity_type = models.CharField(max_length=50)
    scope = models.CharField(max_length=20)
    category = models.CharField(max_length=80)
    activity_date = models.DateField()
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    original_unit = models.CharField(max_length=20)
    normalized_unit = models.CharField(max_length=20)
    normalized_quantity = models.DecimalField(max_digits=14, decimal_places=3)
    emission_factor = models.DecimalField(max_digits=14, decimal_places=6)
    co2e_emissions = models.DecimalField(max_digits=14, decimal_places=3)
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    locked = models.BooleanField(default=False)
    validation_issues = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
