from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import SessionDetails
from .serializers import SessionDetailsSerializer, VideoRoomSerializer
from .permissions import IsPatientOrTherapist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Q
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .hms_api import HMSAPI
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query:
            sessions = SessionDetails.objects.filter(Q(therapist__name__icontains=search_query) | Q(therapist__specialty__icontains=search_query))
            serializer = SessionDetailsSerializer(sessions, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SessionCreateViewset(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Create a new therapy session with optional video conferencing",
        request_body=SessionDetailsSerializer,
        responses={
            201: openapi.Response(
                description="Session created successfully",
                schema=SessionDetailsSerializer
            ),
            400: openapi.Response(
                description="Invalid input data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_name': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            )
        }
    )
    def post(self, request):
        data = request.data.copy()
        data['patient_id'] = request.user.id
        
        # Check if video conferencing is enabled
        is_video_enabled = data.get('is_video_enabled', False)
        
        serializer = SessionDetailsSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save()
            
            # Create video room if enabled
            if is_video_enabled:
                try:
                    hms_api = HMSAPI()
                    room_name = f"session_{session.id}_{session.session_type}"
                    if session.duration == "30":
                        max_duration_seconds = 30 * 60
                    else:
                        max_duration_seconds = 60 * 60
                    
                    if session.session_type == "group":
                        max_participants = 20
                    else:
                        max_participants = 2

                    room_data = hms_api.create_room(
                        room_name=room_name,
                        description=f"Therapy session between {session.patient_id.name} and {session.therapist_id.name}",
                        max_participants=max_participants,
                        max_duration_seconds=max_duration_seconds
                    )
                    
                    # Update session with room information
                    session.room_id = room_data.get('id')
                    session.room_code = room_data.get('room_code')
                    session.room_url = hms_api.get_room_url(room_data.get('id'), room_data.get('room_code'))
                    session.save()
                    
                except Exception as e:
                    logger.error(f"Failed to create video room for session {session.id}: {str(e)}")
                    # Continue without video room if creation fails
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteSessionView(APIView):
    permission_classes = [IsPatientOrTherapist]
    def delete(self, request, pk):
        try:
            session = SessionDetails.objects.get(pk=pk)
            
            # Deactivate video room if exists
            if session.room_id:
                try:
                    hms_api = HMSAPI()
                    hms_api.deactivate_room(session.room_id)
                except Exception as e:
                    logger.error(f"Failed to deactivate room {session.room_id}: {str(e)}")
            
            session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SessionDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class GetAllSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sessions = SessionDetails.objects.all()
        serializer = SessionDetailsSerializer(sessions, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class RetrieveSessionView(APIView):
    permission_classes = [IsPatientOrTherapist]
    def retrieve(self, request, pk):
        try:
            session = SessionDetails.objects.get(pk=pk)
            serializer = SessionDetailsSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SessionDetails.DoesNotExist:
            return Response({'message': 'no session found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateSessionTimeView(APIView):
    @swagger_auto_schema(
        operation_description="Update the start time and end time of a therapy session",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['start_time'],
            properties={
                'start_time': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description="New start time for the session (format: YYYY-MM-DD HH:MM:SS)"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Session time updated successfully",
                schema=SessionDetailsSerializer
            ),
            400: openapi.Response(
                description="Invalid input data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Error message"
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Session not found"
            )
        }
    )
    def patch(self, request, pk):
        session = get_object_or_404(SessionDetails, pk=pk)
        new_start_time = request.data.get('start_time')

        if not new_start_time:
            return Response({"error": "start_time is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_start_time = serializers.DateTimeField().to_internal_value(new_start_time)
        except Exception as e:
            return Response({"error": "Invalid start_time format."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate new end_time based on duration
        if session.duration == "30":
            end_time = new_start_time + timedelta(minutes=30)
        else:
            end_time = new_start_time + timedelta(minutes=60)

        session.start_time = new_start_time
        session.end_time = end_time
        session.save()

        serializer = SessionDetailsSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoRoomView(APIView):
    """Video room management for therapy sessions"""
    permission_classes = [IsPatientOrTherapist]
    
    @swagger_auto_schema(
        operation_description="Get video room details for a session",
        responses={
            200: openapi.Response(
                description="Video room details retrieved successfully",
                schema=VideoRoomSerializer
            ),
            404: openapi.Response(
                description="Session not found or no video room"
            )
        }
    )
    def get(self, request, pk):
        """Get video room details for a session"""
        try:
            session = SessionDetails.objects.get(pk=pk)
            if not session.is_video_enabled or not session.room_id:
                return Response(
                    {"error": "Video conferencing not enabled for this session"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = VideoRoomSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except SessionDetails.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)


class VideoTokenView(APIView):
    """Generate authentication tokens for video conferencing"""
    permission_classes = [IsPatientOrTherapist]
    
    @swagger_auto_schema(
        operation_description="Generate authentication token for video conferencing",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['role'],
            properties={
                'role': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['host', 'guest'],
                    description="User role in the video call"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Token generated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                        'room_id': openapi.Schema(type=openapi.TYPE_STRING, description='Room ID'),
                        'room_code': openapi.Schema(type=openapi.TYPE_STRING, description='Room code'),
                        'room_url': openapi.Schema(type=openapi.TYPE_STRING, description='Room URL')
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid request or video not enabled"
            ),
            404: openapi.Response(
                description="Session not found"
            )
        }
    )
    def post(self, request, pk):
        """Generate authentication token for video conferencing"""
        try:
            session = SessionDetails.objects.get(pk=pk)
            
            if not session.is_video_enabled or not session.room_id:
                return Response(
                    {"error": "Video conferencing not enabled for this session"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            role = request.data.get('role', 'guest')
            if role not in ['host', 'guest']:
                return Response(
                    {"error": "Role must be 'host' or 'guest'"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Determine user name based on role
            if role == 'host':
                user_name = f"Dr. {session.therapist_id.name}"
                user_id = f"therapist_{session.therapist_id.id}"
            else:
                user_name = session.patient_id.name
                user_id = f"patient_{session.patient_id.id}"
            
            try:
                hms_api = HMSAPI()
                token_data = hms_api.generate_token(
                    room_id=session.room_id,
                    user_id=user_id,
                    user_name=user_name,
                    role=role
                )
                
                return Response({
                    'token': token_data.get('token'),
                    'room_id': session.room_id,
                    'room_code': session.room_code,
                    'room_url': session.room_url,
                    'user_name': user_name,
                    'role': role
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f"Failed to generate token for session {pk}: {str(e)}")
                return Response(
                    {"error": "Failed to generate authentication token"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except SessionDetails.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)


class EnableVideoView(APIView):
    """Enable video conferencing for an existing session"""
    permission_classes = [IsPatientOrTherapist]
    
    @swagger_auto_schema(
        operation_description="Enable video conferencing for an existing session",
        responses={
            200: openapi.Response(
                description="Video conferencing enabled successfully",
                schema=VideoRoomSerializer
            ),
            400: openapi.Response(
                description="Video already enabled or session not found"
            )
        }
    )
    def post(self, request, pk):
        """Enable video conferencing for an existing session"""
        try:
            session = SessionDetails.objects.get(pk=pk)
            
            if session.is_video_enabled:
                return Response(
                    {"error": "Video conferencing already enabled for this session"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                hms_api = HMSAPI()
                room_name = f"session_{session.id}_{session.session_type}"
                room_data = hms_api.create_room(
                    room_name=room_name,
                    description=f"Therapy session between {session.patient_id.name} and {session.therapist_id.name}",
                    max_participants=2
                )
                
                # Update session with room information
                session.room_id = room_data.get('id')
                session.room_code = room_data.get('room_code')
                session.room_url = hms_api.get_room_url(room_data.get('id'), room_data.get('room_code'))
                session.is_video_enabled = True
                session.save()
                
                serializer = VideoRoomSerializer(session)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f"Failed to enable video for session {pk}: {str(e)}")
                return Response(
                    {"error": "Failed to enable video conferencing"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except SessionDetails.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)


class RoomParticipantsView(APIView):
    """Get active participants in a video room"""
    permission_classes = [IsPatientOrTherapist]
    
    @swagger_auto_schema(
        operation_description="Get active participants in the video room",
        responses={
            200: openapi.Response(
                description="Active participants retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'participants': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'user_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'role': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Session not found or no video room"
            )
        }
    )
    def get(self, request, pk):
        """Get active participants in the video room"""
        try:
            session = SessionDetails.objects.get(pk=pk)
            
            if not session.is_video_enabled or not session.room_id:
                return Response(
                    {"error": "Video conferencing not enabled for this session"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                hms_api = HMSAPI()
                peers_data = hms_api.get_active_peers(session.room_id)
                
                participants = []
                for peer in peers_data.get('peers', []):
                    participants.append({
                        'user_id': peer.get('user_id'),
                        'user_name': peer.get('user_name'),
                        'role': peer.get('role')
                    })
                
                return Response({
                    'participants': participants,
                    'total_participants': len(participants)
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f"Failed to get participants for session {pk}: {str(e)}")
                return Response(
                    {"error": "Failed to get room participants"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except SessionDetails.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
