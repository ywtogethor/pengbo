from django.db import models

# Create your models here.

class One(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

class Two(models.Model):
    email = models.EmailField()
    website = models.URLField()

class Three(models.Model):
    address = models.CharField(max_length=255)

class Four(models.Model):
    brand = models.CharField(max_length=255)
