from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = 'patients'

router = DefaultRouter()
router.register(r'patients',PatientViewset,basename='patient')

urlpatterns = [
    path('',include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]