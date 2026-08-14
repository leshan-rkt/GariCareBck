from django.db import models
from django.db import models
from django.conf import settings
from cars.models import Car
from maintenance.models import MaintenanceRecord

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending — PIN not entered yet'),
        ('COMPLETED', 'Payment Successful'),
        ('FAILED', 'Payment Failed / Cancelled'),
    ]

    # WHO paid & WHAT for
    maintenance_record = models.ForeignKey(
        MaintenanceRecord, 
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payer_phone = models.CharField("Payer's Phone", max_length=20)  # User's phone
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # WHO gets the money
    recipient_name = models.CharField("Mechanic/Garage", max_length=100, blank=True)
    recipient_phone = models.CharField("Mechanic Phone/Paybill", max_length=20, blank=True)
    
    # M-Pesa transaction details
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    mpesa_receipt = models.CharField("M-Pesa Receipt No.", max_length=50, blank=True, null=True)
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_desc = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"KES {self.amount} → {self.recipient_name or 'Garage'} — {self.get_status_display()}"