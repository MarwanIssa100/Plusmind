from django.db import models
from patients.models import Patient
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator , MaxValueValidator
from django.conf import settings
from apps.Notes.models import Notes 
from datetime import datetime


class Therapist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='therapist/photo/',null=True,blank=True)
    working_hours = models.TimeField(default=datetime.now)
    joining_date = models.DateTimeField(auto_now_add=True)
    certificates = models.ImageField(upload_to='therapist/certificates/',null=True,blank=True)
    experience = models.TextField(null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
    def getAVGRating(self):
        reviews = TherapistReview.objects.filter(therapist=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
    
class TherapistContact(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE,related_name='therapist_contact')
    country_code = models.CharField(max_length=5)
    contact = models.CharField(max_length=20)
    
class TherapistReview(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE,related_name='therapist_reviews')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
class TherapistConclusions(Notes):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE,related_name='therapist_conclusions')
    session = models.ForeignKey('sessionDetails.SessionDetails', on_delete=models.CASCADE,related_name='session_conclusions',null=True,blank=True)
    
