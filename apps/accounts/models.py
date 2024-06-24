from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField()
    firstname = models.CharField(null=True, max_length=255)
    lastname = models.CharField(null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(null=True, max_length=20)
