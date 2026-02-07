from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    bot_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
