from django.db import models
from django.db import models
from django.conf import settings
from cars.models import Car

# Create your models here.
class MaintenanceRecord(models.Model):
    class ServiceType(models.TextChoices):
       SERVICE_TYPES = [
            ('ROUTINE', 'Routine Maintenance'),
            ('REPAIR', 'Repair'),
            ('OIL_CHANGE', 'Oil Change'),
            ('TYRES', 'Tyres / Alignment'),
            ('INSURANCE', 'Insurance'),
            ('OTHER', 'Other'),
        ]
       
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='maintenance_records')
    service_date = models.DateField()
    mileage_at_service = models.PositiveIntegerField()
    service_type = models.CharField(max_length=20, choices=ServiceType.choices)
    description = models.TextField()
    parts_replaced = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    service_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-service_date']

    def __str__(self):
        return f"{self.car.license_plate} — {self.service_type} — KES {self.cost}"