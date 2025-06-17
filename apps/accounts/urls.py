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
    path('login/therapist/', TherapistLoginView.login, name='therapist-login'),
    path('login/patient/', PatientLoginView.login, name='patient-login'),
    path('logout/therapist/', TherapistRegisterViewSet.logout, name='therapist-logout'),
    path('logout/patient/', PatientRegisterViewSet.logout, name='patient-logout'),
    path('password-reset/', PasswordResetViewSet.request_reset, name='password-reset'),

]
