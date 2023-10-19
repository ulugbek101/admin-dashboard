import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile-pictures/',
                                        null=True,
                                        blank=True,
                                        default='profile-pictures/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
