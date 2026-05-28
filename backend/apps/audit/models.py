from django.db import models

from apps.normalization.models import NormalizedActivity


class AuditLog(models.Model):
    activity = models.ForeignKey(NormalizedActivity, on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=50)
    previous_value = models.JSONField(default=dict, blank=True)
    new_value = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
