from django.db import models
from django.db import models
from django.conf import settings
from cars.models import Car
from maintenance.models import MaintenanceRecord

# Create your models here.
class MpesaTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='mpesa_transactions')
    merchant_request_id = models.CharField(max_length=100, unique=True)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    account_reference = models.CharField(max_length=100)
    transaction_desc = models.CharField(max_length=255)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    maintenance_record = models.ForeignKey(MaintenanceRecord, on_delete=models.SET_NULL, null=True, blank=True)

    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    mpesa_receipt_number = models.CharField(max_length=50, null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone_number} — KES {self.amount} — {self.status}"