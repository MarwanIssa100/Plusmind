from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .permissions import IsTherapist
from sessionDetails.serializers import SessionDetailsSerializer
from sessionDetails.models import SessionDetails

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


class GetTherapistSessions(APIView):
    permission_classes = [IsTherapist]

    def get(self, request, *args, **kwargs):
        therapist = request.user.therapist
        sessions = SessionDetails.objects.filter(therapist=therapist)
        serializer = SessionDetailsSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)