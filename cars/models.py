from django.db import models
from django.db import models
from django.conf import settings

# Create your models here.
class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=30)
    vin = models.CharField(max_length=50, blank=True, null=True)
    current_mileage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['make', 'model', '-year']

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"