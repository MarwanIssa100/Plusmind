from rest_framework import serializers
from rest_framework.authentication import authenticate
from .models import Therapist, TherapistReview, TherapistContact
from django.contrib.auth.models import User

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
        fields = ['specialty','photo','working_hours','joining_date','certificates','experience','reviews','contact']


class TherapistRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    confirm_password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    class Meta:
        model = Therapist
        fields = ['specialty', 'photo', 'working_hours', 'joining_date', 'password', 'confirm_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password and confirm password does not match")
        return attrs
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password
        )
        validated_data.pop('confirm_password')  
        password = validated_data.pop('password')
        therapist = Therapist.objects.create(user=user, **validated_data)
        therapist.save()
        return therapist
    
class TherapistLoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    class Meta:
        model = Therapist
        fields = ['username', 'password']
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    {"non_field_errors": "Unable to log in with provided credentials."}
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    {"non_field_errors": "User account is disabled."}
                )
            try:
                therapist = Therapist.objects.get(user=user)
            except Therapist.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": "Therapist profile not found."}
                )
            
        else:
            raise serializers.ValidationError(
                {"non_field_errors": 'Must include "email" and "password".'}
            )
            
        return attrs
    