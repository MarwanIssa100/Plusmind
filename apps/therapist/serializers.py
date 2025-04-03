from rest_framework import serializers
from .models import Therapist, TherapistReview, TherapistContact

class TherapistReviewSerializer(serializers.ModelSerializer):
    therapist_name = serializers.CharField(source='therapist.name',read_only=True)
    class Meta:
        model = TherapistReview
        fields = ['id', 'therapist_name', 'patient', 'review', 'rating']
class TherapistContactSerializer(serializers.ModelSerializer):
    therapist_name = serializers.CharField(source='therapist.name',read_only=True)
    class Meta:
        model = TherapistContact
        fields = ['id','therapist_name','country_code','contact']
class TherapistSerializer(serializers.ModelSerializer):
    reviews = TherapistReviewSerializer(source='therapist_reviews',read_only=True,many=True)
    contact = TherapistContactSerializer(source='therapist_contact',read_only=True,many=True)
    class Meta:
        model = Therapist
        fields = '__all__'
