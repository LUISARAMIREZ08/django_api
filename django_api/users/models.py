from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# This is a custom user model that extends the default Django user model.
class User(AbstractUser):
    pass