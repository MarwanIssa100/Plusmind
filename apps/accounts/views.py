from rest_framework import viewsets ,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    
    @swagger_auto_schema(
        method='post',
        operation_summary="Logout Therapist",
        tags=['Accounts'],
        operation_description="Blacklist the provided refresh token to log out the therapist.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Refresh token to be blacklisted',
                    example='eyJ0eXAiOiJKV1QiLCJh...'
                ),
            },
        ),
        responses={
            205: openapi.Response(
                description="Logout successful",
                examples={
                    "application/json": {
                        "detail": "Successfully logged out."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid or expired refresh token",
                examples={
                    "application/json": {
                        "error": "Token is invalid or expired"
                    }
                }
            ),
        }
    )
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

    @swagger_auto_schema(
        method='post',
        operation_summary="Logout Patient",
        tags=['Accounts'],
        operation_description="Blacklist the provided refresh token to log out the patient.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="JWT refresh token",
                    example="eyJ0eXAiOiJKV1QiLCJhbGc..."
                )
            }
        ),
        responses={
            205: openapi.Response(
                description="Logout successful",
                examples={"application/json": {"detail": "Successfully logged out."}}
            ),
            400: openapi.Response(
                description="Logout error",
                examples={"application/json": {"error": "Token is invalid or expired"}}
            )
        }
    )
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
    
    @swagger_auto_schema(
        operation_summary="Therapist Login",
        tags=['Accounts'],
        operation_description="Authenticate therapist and return access/refresh tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="therapist@example.com"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, example="securepassword123")
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "therapist": {
                            "id": 1,
                            "user": {
                                "id": 5,
                                "email": "therapist@example.com"
                            },
                            "specialty": "Cognitive Therapy"
                        },
                        "tokens": {
                            "access": "eyJ0eXAiOiJKV1QiLCJh...",
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials or validation errors",
                examples={
                    "application/json": {
                        "non_field_errors": ["Invalid credentials for therapist."]
                    }
                }
            )
        }
    )
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

    @swagger_auto_schema(
        operation_summary="Patient Login",
        tags=['Accounts'],
        operation_description="Authenticate patient and return access/refresh tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="patient@example.com"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, example="strongpassword123")
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "patient": {
                            "id": 2,
                            "user": {
                                "id": 7,
                                "email": "patient@example.com"
                            },
                            "address": "Cairo, Egypt",
                            "Birth_date": "1990-05-01"
                        },
                        "tokens": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials or validation errors",
                examples={
                    "application/json": {
                        "non_field_errors": ["Invalid credentials for Patient."]
                    }
                }
            )
        }
    )    
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

    @swagger_auto_schema(
        operation_summary="Request Password Reset",
        tags=['Accounts'],
        operation_description="Send password reset link to the provided email address if the user exists.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="user@example.com")
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset link sent",
                examples={
                    "application/json": {
                        "detail": "Password reset link sent to your email."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid request",
                examples={
                    "application/json": {
                        "email": ["User with this email does not exist."]
                    }
                }
            )
        }
    )
    @action(detail=False, methods=["post"])
    def request_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)