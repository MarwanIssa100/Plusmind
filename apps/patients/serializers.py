from .models import Patient
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate


class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    confirm_password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    class Meta:
        model = Patient
        fields = ['address', 'Birth_date', 'gender', 'password', 'confirm_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password and confirm password does not match")
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        password = validated_data.pop('password')
        patient = Patient(**validated_data)
        patient.set_password(password)  
        patient.save()
        return patient
    
class PatientLoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    class Meta:
        model = Patient
        fields = ['username', 'password']
        
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
            
        else:
            raise serializers.ValidationError(
                {"non_field_errors": 'Must include "email" and "password".'}
            )
            
        return attrs
    