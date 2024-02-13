from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser, models.Model):
    api_id = models.IntegerField(default=None)