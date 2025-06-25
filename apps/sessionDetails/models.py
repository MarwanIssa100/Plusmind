from django.db import models
from accounts.models import Therapist, Patient


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
    
    # 100ms.live video conferencing fields
    room_id = models.CharField(max_length=255, null=True, blank=True, help_text="100ms room ID")
    room_code = models.CharField(max_length=255, null=True, blank=True, help_text="100ms room code")
    room_url = models.URLField(null=True, blank=True, help_text="100ms room URL")
    is_video_enabled = models.BooleanField(help_text="Whether video conferencing is enabled for this session")
    # review = models.ForeignKey(Reviews, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
