from .managers import CustomTherapistManager
from django.db import models
from patients.models import Patient
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator , MaxValueValidator


class Therapist(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'),unique=True)
    specialty = models.CharField(max_length=100)
    working_hours = models.TimeField()
    joining_date = models.DateTimeField(auto_now_add=True)
    certificates = models.ImageField(upload_to='therapist/certificates/',null=True,blank=True)
    experience = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = CustomTherapistManager()

    def __str__(self):
        return self.name
    def getAVGRating(self):
        reviews = TherapistReviwe.objects.filter(therapist=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
    
class TherapistContact(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5)
    contact = models.CharField(max_length=20)
    
class TherapistReviwe(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
