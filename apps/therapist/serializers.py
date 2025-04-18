from rest_framework import serializers
from .models import Therapist, TherapistReview, TherapistContact

class TherapistReviewSerializer(serializers.ModelSerializer):
    therapist_name = serializers.CharField(source='therapist.name',read_only=True)
    class Meta:
        model = TherapistReview
        fields = ['therapist_name', 'patient', 'review', 'rating']
class TherapistContactSerializer(serializers.ModelSerializer):
    therapist_name = serializers.CharField(source='therapist.name',read_only=True)
    class Meta:
        model = TherapistContact
        fields = ['therapist_name','country_code','contact']

class TherapistAdminSerializer(serializers.ModelSerializer):
    reviews = TherapistReviewSerializer(source='therapist_reviews',read_only=True,many=True)
    contact = TherapistContactSerializer(source='therapist_contact',read_only=True,many=True)
    class Meta:
        model = Therapist
        fields = '__all__'


class TherapistSerializer(serializers.ModelSerializer):
    reviews = TherapistReviewSerializer(source='therapist_reviews',read_only=True,many=True)
    contact = TherapistContactSerializer(source='therapist_contact',read_only=True,many=True)
    class Meta:
        model = Therapist
        fields = ['name','email','specialty','photo','working_hours','joining_date','certificates','experience','is_active','reviews','contact']

    def validate_email(self, value):
        if Therapist.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_working_hours(self, value):
        if value.hour < 0 or value.hour > 23 :
            raise serializers.ValidationError("Invalid working hours")
        return value
    

    def validate(self, attrs):
        speciality = attrs.get('specialty')
        if speciality and len(speciality) < 5:
            raise serializers.ValidationError("Speciality must be at least 5 characters")
        
        name = attrs.get('name')
        if not name or name.strip() == '':
            raise serializers.ValidationError("Name must be at least 5 characters")
        return attrs

    
    def create(self, validated_data):
        therapist = Therapist.objects.create(**validated_data)
        return therapist
