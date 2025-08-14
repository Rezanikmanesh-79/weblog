from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        AUTHOR = 'author'
        READER = 'reader'

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.READER
    )

def save(self, *args, **kwargs):
    if self.role == self.Role.ADMIN:
        self.is_staff = True
        self.is_superuser = True
    elif self.role == self.Role.AUTHOR:
        self.is_staff = True
        self.is_superuser = False
    else: 
        self.is_staff = False
        self.is_superuser = False

    super().save(*args, **kwargs)

def __str__(self):
    return f"{self.username} ({self.role})"
