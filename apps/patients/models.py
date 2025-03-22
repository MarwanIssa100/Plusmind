from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_countries.fields import CountryField


# Create your models here.
class Patient(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    Birth_date = models.DateTimeField(auto_now_add=False)
    gender = models.enums.Choices(("male", "female"))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.name
    
class PatientContact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    country = CountryField(blank_label="(select country)")
    contact = models.CharField(max_length=20)
