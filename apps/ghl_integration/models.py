from django.db import models

from apps.accounts.models import ClientProfile
from common.models import TimeStampedModel


class GhlContactMapping(TimeStampedModel):
    client = models.OneToOneField(ClientProfile, on_delete=models.CASCADE, related_name="ghl_mapping")
    ghl_contact_id = models.CharField(max_length=128, unique=True)
    location_id = models.CharField(max_length=128, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.ghl_contact_id
