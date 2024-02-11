from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    date_of_birth = models.DateField(blank=True, null=True)

    class DoesNotExist(Exception):
        def __init__(self, message="does not exist user"):
            super().__init__(message)

    def __str__(self):
        return self.email