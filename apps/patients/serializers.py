from .models import Patient
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from django.contrib.auth.models import User
from datetime import datetime


class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    confirm_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Patient
        fields = ['email', 'name', 'address', 'Birth_date', 'gender', 'password', 'confirm_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password do not match")
        return attrs
        
    def create(self, validated_data):
        # Remove password fields from validated_data
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        Birth_date = validated_data.pop('Birth_date').strftime('%Y-%m-%d')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password
        )
        
        # Create Patient instance
        patient = Patient.objects.create(
            user=user,
            Birth_date=Birth_date,
            **validated_data
        )
        
        return patient
    
class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Authenticate against the User model
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
                
            # Get the patient instance
            try:
                patient = Patient.objects.get(user=user)
            except Patient.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": "Patient profile not found."}
                )
            
            # Add patient to validated data
            attrs['patient'] = patient
            attrs['user'] = user
            
        else:
            raise serializers.ValidationError(
                {"non_field_errors": 'Must include "email" and "password".'}
            )
            
        return attrs
    