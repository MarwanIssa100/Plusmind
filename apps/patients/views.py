from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
class PatientViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'login':
            return PatientLoginSerializer
        return PatientRegisterSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated]
        return [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        
        # Generate tokens for immediate login after registration
        user = patient.user
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'patient': PatientRegisterSerializer(patient).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }
        
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = PatientLoginSerializer(data=request.data, context={'request': request})
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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"detail": "Successfully logged out."},
                    status=status.HTTP_205_RESET_CONTENT
                )
            return Response(
                {"detail": "Refresh token was not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientRegisterSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )