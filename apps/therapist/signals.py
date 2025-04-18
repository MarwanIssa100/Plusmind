from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Therapist

User = get_user_model()

@receiver(post_save, sender=User)
def create_therapist_profile(sender, instance, created, **kwargs):
    if created:
        Therapist.objects.create(user=instance) 