from django.db import models

from apps.accounts.models import ClientProfile
from common.models import TimeStampedModel


class KpiSnapshot(TimeStampedModel):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="kpi_snapshots", null=True, blank=True)
    metric_key = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=14, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=["metric_key", "period_start", "period_end"]),
        ]

    def __str__(self):
        return f"{self.metric_key}: {self.metric_value}"
