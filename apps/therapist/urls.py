from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'therapist'

router = DefaultRouter()
router.register(r'therapists',TherapistViewset,basename='therapist')
router.register(r'contacts',TherapistContactViewset,basename='contact')
router.register(r'reviews',TherapistReviewViewset,basename='review')

urlpatterns = [
    path('',include(router.urls)),
    path('login/therapist/', TherapistViewset.login, name='therapist-login'),
]