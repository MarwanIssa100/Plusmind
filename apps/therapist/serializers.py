from rest_framework import serializers
from rest_framework.authentication import authenticate
from .models import Therapist, TherapistReview, TherapistContact , CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TherapistTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 

    def validate(self, attrs):
        # Authenticate user
        data = super().validate(attrs)
        user = self.user

        # Check if user is a therapist
        if not hasattr(user, 'therapist'):
            raise serializers.ValidationError("No therapist profile associated with this user.")

        # Add custom claims
        data['role'] = 'therapist'
        data['therapist_id'] = user.therapist.id
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = 'therapist'
        return token
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'name', 'gender', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


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


class TherapistRegisterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    confirm_password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
    class Meta:
        model = Therapist
        fields = ['user','specialty', 'photo', 'working_hours', 'joining_date', 'certificates' ,'experience','password','confirm_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password and confirm password does not match")
        return attrs
        
def create(self, validated_data):
    user_data = validated_data.pop('user')
    password = validated_data.pop('password')
    validated_data.pop('confirm_password', None)

    email = user_data.get('email')

    if CustomUser.objects.filter(email=email).exists():
        raise serializers.ValidationError({'email': 'A user with this email already exists.'})

    user_data.pop('password', None)
    user_data['role'] = 'therapist'

    user = CustomUser.objects.create_user(password=password, **user_data)

    # Extra safety check (should not trigger unless logic is broken)
    if hasattr(user, 'therapist'):
        raise serializers.ValidationError("This user already has a therapist profile.")

    therapist = Therapist.objects.create(user=user, **validated_data)
    return therapist
    
# # class TherapistLoginSerializer(serializers.ModelSerializer):
#     username = serializers.EmailField()
#     password = serializers.CharField(write_only=True , min_length=8 , max_length=128)
#     class Meta:
#         model = Therapist
#         fields = ['username', 'password']
        
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
        
#         if email and password:
#             user = authenticate(
#                 request=self.context.get('request'),
#                 username=email,
#                 password=password
#             )
            
#             if not user:
#                 raise serializers.ValidationError(
#                     {"non_field_errors": "Unable to log in with provided credentials."}
#                 )
#             if not user.is_active:
#                 raise serializers.ValidationError(
#                     {"non_field_errors": "User account is disabled."}
#                 )
#             try:
#                 therapist = Therapist.objects.get(user=user)
#             except Therapist.DoesNotExist:
#                 raise serializers.ValidationError(
#                     {"non_field_errors": "Therapist profile not found."}
#                 )
            
#         else:
#             raise serializers.ValidationError(
#                 {"non_field_errors": 'Must include "email" and "password".'}
#             )
            
#         return attrs
    