from typing import List
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500, unique=True)
    password = models.CharField(max_length=500)
    username = None

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []