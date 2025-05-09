from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from apps.Notes.models import Notes
from datetime import datetime


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    GENDER = (("male", "male"), ("female", "female"))
    address = models.TextField()
    Birth_date = models.DateField(auto_now_add=False)
    gender = models.CharField(max_length=10, choices=GENDER)
    
    def __str__(self):
        return self.name
    
class PatientContact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    country = CountryField(blank_label="(select country)")
    counrty_code = models.CharField(max_length=5)
    contact = models.CharField(max_length=20)
    
class PatientNotes(Notes):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
