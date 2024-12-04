from django.db import models

# Create your models here.
class hospital(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    add = models.TextField()
    phone = models.TextField()
    time = models.TextField()