from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=100)
    content = MDTextField()
    
    class Meta:
        abstract = True

