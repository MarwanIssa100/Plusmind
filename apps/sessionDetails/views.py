from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import SessionDetails
from .serializers import SessionDetailsSerializer
from .permissions import IsPatientOrTherapist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Q
from datetime import timedelta

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
    def post(self, request):
        serializer = SessionDetailsSerializer(data=request.data)
        # serializer.Meta.patient_id = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteSessionView(APIView):
    permission_classes = [IsPatientOrTherapist]
    def delete(self, request, pk):
        try:
            session = SessionDetails.objects.get(pk=pk)
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
