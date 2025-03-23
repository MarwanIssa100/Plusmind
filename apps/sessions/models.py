from django.db import models
from therapist.models import Therapist
from patients.models import Patient
from reviews.models import Reviews

# Create your models here.

class Session(models.Model):
    sessionChoices = (("consultation", "Consultation"), ("treatment", "Treatment"), ("group", "Group"))
    id = models.AutoField(primary_key=True)
    session_type = models.Choices(sessionChoices)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist_id = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
