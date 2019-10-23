from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Author(AbstractUser):

    def __str__(self):
        return getattr(self, 'username', str(self.pk)) 
