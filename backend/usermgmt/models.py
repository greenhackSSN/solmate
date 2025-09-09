from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('therapist', 'Therapist'),
        ('supervisor', 'Supervisor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    language = models.CharField(max_length=50, blank=True, null=True)  # For AI matching
    location = models.CharField(max_length=100, blank=True, null=True) # For AI matching
