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

    def __str__(self):
        return self.email