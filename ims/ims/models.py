from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.username}'