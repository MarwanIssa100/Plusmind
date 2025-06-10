from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from accounts.models import Therapist
from accounts.serializers import *
# from .permissions import IsTherapist
from sessionDetails.serializers import SessionDetailsSerializer
from sessionDetails.models import SessionDetails    
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TherapistViewset(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistRegisterSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        # elif self.action in ['update','partial_update','destroy']:
        #     # return [IsTherapist()]
        # else:
        #     return [IsAuthenticated()]
        
        
#     def get_serializer_class(self):
#         if self.request.user.is_staff or self.request.user.is_superuser:
#             return TherapistAdminSerializer
#         return TherapistRegisterSerializer
    
#     def login(self, request):
#         serializer = TherapistTokenObtainPairSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
        
#         therapist = Therapist.objects.get(user=serializer.validated_data['user'])
#         refresh = RefreshToken.for_user(therapist.user)
        
#         return Response({
#             'therapist': TherapistRegisterSerializer(therapist).data,
#             'tokens': {
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#             }
#         })

# class TherapistContactViewset(viewsets.ModelViewSet):
#     queryset = TherapistContact.objects.all()
#     serializer_class = TherapistContactSerializer

#     def get_permissions(self):
#         if self.action == 'create':
#             return [AllowAny()]
#         elif self.action in ['update','partial_update','destroy']:
#             return [IsTherapist()]
#         else:
#             return [IsAuthenticated()]

# class TherapistReviewViewset(viewsets.ModelViewSet):
#     queryset = TherapistReview.objects.all()
#     serialzer_class = TherapistReviewSerializer

#     def get_permissions(self):
#         if self.action == 'create':
#             return [AllowAny()]
#         elif self.action in ['update','partial_update','destroy']:
#             return [IsTherapist()]
#         else:
#             return [IsAuthenticated()]


class GetTherapistSessions(APIView):
    # permission_classes = [IsTherapist]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all sessions for the authenticated therapist",
        responses={
            200: openapi.Response(
                description="List of therapist's sessions retrieved successfully",
                schema=SessionDetailsSerializer(many=True)
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(
                description="User is not a therapist"
            )
        },
        tags=['Therapist Sessions']
    )
    def get(self, request, *args, **kwargs):
        therapist = request.user.id
        sessions = SessionDetails.objects.filter(therapist_id=therapist)
        serializer = SessionDetailsSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)