from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'therapist'


urlpatterns = [
    path('sessions/', GetTherapistSessions.as_view(), name='therapist-sessions'),
]