from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class CustomUser(AbstractUser):
    GENDER = (("male", "male"), ("female", "female"))
    ROLES = (("therapist", "therapist"), ("patient", "patient"))

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLES)
    gender = models.CharField(max_length=10, choices=GENDER)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    Birth_date = models.DateField(auto_now_add=False)
    
    
class Therapist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='therapist/photo/',null=True,blank=True)
    working_hours = models.TimeField(default=datetime.now)
    joining_date = models.DateTimeField(auto_now_add=True)
    certificates = models.ImageField(upload_to='therapist/certificates/',null=True,blank=True)
    experience = models.TextField(null=True,blank=True)
