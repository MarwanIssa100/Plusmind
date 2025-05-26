from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TherapistRegisterViewSet,
    PatientRegisterViewSet,
    TherapistLoginView,
    PatientLoginView ,
    PasswordResetViewSet
)
app_name = 'accounts'

router = DefaultRouter()
router.register(r'register/therapist', TherapistRegisterViewSet, basename='register-therapist')
router.register(r'register/patient', PatientRegisterViewSet, basename='register-patient')
router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

urlpatterns = [
    path('', include(router.urls)),
    path('login/therapist/', TherapistLoginView.as_view(), name='therapist-login'),
    path('login/patient/', PatientLoginView.as_view(), name='patient-login'),
]
