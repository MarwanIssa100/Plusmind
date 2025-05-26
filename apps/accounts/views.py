from rest_framework import viewsets ,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Therapist, Patient
from .serializers import (
    TherapistRegisterSerializer,
    PatientRegisterSerializer,
    TherapistTokenObtainPairSerializer,
    PatientTokenObtainPairSerializer ,
    PasswordResetSerializer
)

class TherapistRegisterViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistRegisterSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class PatientRegisterViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class TherapistLoginView(TokenObtainPairView):
    serializer_class = TherapistTokenObtainPairSerializer
    
    @action(detail=False , methods=['post'], permission_classes=[IsAuthenticated])
    def login(self, request):
        serializer = TherapistTokenObtainPairSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        therapist = Therapist.objects.get(user=serializer.validated_data['user'])
        refresh = RefreshToken.for_user(therapist.user)
        
        return Response({
            'therapist': TherapistRegisterSerializer(therapist).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })


class PatientLoginView(TokenObtainPairView):
    serializer_class = PatientTokenObtainPairSerializer
    
    @action(detail=False , methods=['post'], permission_classes=[IsAuthenticated])
    def login(self, request):
        serializer = PatientTokenObtainPairSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        patient = Patient.objects.get(user=serializer.validated_data['user'])
        refresh = RefreshToken.for_user(patient.user)
        
        return Response({
            'patient': PatientRegisterSerializer(patient).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })


class PasswordResetViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def request_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)