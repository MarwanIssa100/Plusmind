from django.db import models
from therapist.models import Therapist
from patients.models import Patient
from reviews.models import Reviews

# Create your models here.

class SessionDetails(models.Model):
    SESSION_CHOICES = (("consultation", "Consultation"), ("treatment", "Treatment"), ("group", "Group"))
    status = (("pending", "Pending"), ("completed", "Completed"), ("cancelled", "Cancelled"))
    duration_choices = (("30", "30"), ("60", "60"))
    id = models.AutoField(primary_key=True)
    session_type = models.CharField(max_length=20, choices=SESSION_CHOICES)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist_id = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status, default="pending")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.CharField(max_length=2, choices=duration_choices , default="30")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
