from django.db import models
from therapist.models import Therapist
from patients.models import Patient
from reviews.models import Reviews

# Create your models here.

class SessionDetails(models.Model):
    SESSION_CHOICES = (("consultation", "Consultation"), ("treatment", "Treatment"), ("group", "Group"))
    id = models.AutoField(primary_key=True)
    session_type = models.CharField(max_length=20, choices=SESSION_CHOICES)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist_id = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
