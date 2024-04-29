from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.username
