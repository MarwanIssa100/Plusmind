from django.shortcuts import render
from rest_framework.views import APIView
from .models import SessionDetails
from .serializers import SessionDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
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
    

