from django.db import models
import datetime

# Create your models here.

class Lager(models.Model):
    id = models.AutoField(primary_key=True)
    Barcode = models.CharField(max_length=30)
    Bezeichnung = models.CharField(max_length=25)
    Kategorie = models.CharField(max_length=20)
    Lagerbestand = models.IntegerField(max_length=4)
    Mindestbestand = models.IntegerField(max_length=4)

    def __str__(self):
        return f'{self.Bezeichnung}'