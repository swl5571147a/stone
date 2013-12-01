from django.db import models

# Create your models here.
class Note(models.Model):
    os = models.CharField(max_length=20)
    sn= models.CharField(max_length=25)
