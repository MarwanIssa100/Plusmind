# from .models import Patient
# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.authentication import authenticate
# from datetime import datetime
# from therapist.models import CustomUser
# from therapist.serializers import CustomUserSerializer


# class PatientTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = 'email' 

#     def validate(self, attrs):
#         # Authenticate user
#         data = super().validate(attrs)
#         user = self.user

#         # Check if user is a patient
#         if not hasattr(user, 'patient'):
#             raise serializers.ValidationError("No patient profile associated with this user.")

#         # Add custom claims
#         data['role'] = 'patient'
#         data['therapist_id'] = user.patient.user_id
#         return data
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims
#         token['role'] = 'patient'
#         return token

# class PatientRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8, max_length=128)
#     confirm_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
#     user = CustomUserSerializer()

#     class Meta:
#         model = Patient
#         fields = [ 'user', 'address', 'Birth_date', 'password', 'confirm_password']
        
#     def validate(self, attrs):
#         password = attrs.get('password')
#         confirm_password = attrs.get('confirm_password')
#         if password != confirm_password:
#             raise serializers.ValidationError("Password and confirm password do not match")
#         return attrs
        
#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         validated_data.pop('confirm_password', None)
#         validated_data.pop('password', None)
#         user_data['role'] = 'patient'
#         user = CustomUser.objects.create_user(**user_data)
#         patient = Patient.objects.create(user=user, **validated_data)
#         return patient
        
#         return patient
    
# # class PatientLoginSerializer(serializers.Serializer):
# #     email = serializers.EmailField()
# #     password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    
# #     def validate(self, attrs):
# #         email = attrs.get('email')
# #         password = attrs.get('password')
        
# #         if email and password:
# #             # Authenticate against the User model
# #             user = authenticate(
# #                 request=self.context.get('request'),
# #                 username=email,
# #                 password=password
# #             )
            
# #             if not user:
# #                 raise serializers.ValidationError(
# #                     {"non_field_errors": "Unable to log in with provided credentials."}
# #                 )
# #             if not user.is_active:
# #                 raise serializers.ValidationError(
# #                     {"non_field_errors": "User account is disabled."}
# #                 )
                
# #             # Get the patient instance
# #             try:
# #                 patient = Patient.objects.get(user=user)
# #             except Patient.DoesNotExist:
# #                 raise serializers.ValidationError(
# #                     {"non_field_errors": "Patient profile not found."}
# #                 )
            
# #             # Add patient to validated data
# #             attrs['patient'] = patient
# #             attrs['user'] = user
            
# #         else:
# #             raise serializers.ValidationError(
# #                 {"non_field_errors": 'Must include "email" and "password".'}
# #             )
            
# #         return attrs
    