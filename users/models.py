from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        SACCO = 'SACCO', 'SACCO / Fleet Operator'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.INDIVIDUAL)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # SACCO-only fields
    sacco_name = models.CharField(max_length=100, blank=True, null=True)
    sacco_registration = models.CharField(max_length=50, blank=True, null=True)

    @property
    def is_sacco(self):
        return self.role == self.Role.SACCO

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"