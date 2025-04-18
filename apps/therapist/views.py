from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import *
from .serializers import *
from .permissions import IsTherapist

class TherapistViewset(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update','partial_update','destroy']:
            return [IsTherapist()]
        else:
            return [IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return TherapistAdminSerializer
        return TherapistSerializer

class TherapistContactViewset(viewsets.ModelViewSet):
    queryset = TherapistContact.objects.all()
    serializer_class = TherapistContactSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update','partial_update','destroy']:
            return [IsTherapist()]
        else:
            return [IsAuthenticated()]

class TherapistReviewViewset(viewsets.ModelViewSet):
    queryset = TherapistReview.objects.all()
    serialzer_class = TherapistReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update','partial_update','destroy']:
            return [IsTherapist()]
        else:
            return [IsAuthenticated()]
