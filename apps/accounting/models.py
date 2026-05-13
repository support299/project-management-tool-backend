from django.db import models

from apps.accounts.models import ClientProfile
from common.models import TimeStampedModel


class Invoice(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        PAID = "paid", "Paid"
        VOID = "void", "Void"

    client = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, related_name="invoices")
    invoice_number = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.invoice_number


class Expense(TimeStampedModel):
    vendor_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.vendor_name} - {self.amount}"
