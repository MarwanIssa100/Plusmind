from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializers import *

class TherapistViewset(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

class TherapistContactViewset(viewsets.ModelViewSet):
    queryset = TherapistContact.objects.all()
    serializer_class = TherapistContactSerializer

class TherapistReviewViewset(viewsets.ModelViewSet):
    queryset = TherapistReview.objects.all()
    serialzer_class = TherapistReviewSerializer
