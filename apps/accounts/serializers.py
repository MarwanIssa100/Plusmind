from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Therapist, Patient
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
class TherapistTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user or not isinstance(user, CustomUser) or user.role != 'therapist':
            raise serializers.ValidationError("Invalid credentials for therapist.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Attach the validated user to self.user as expected by super()
        self.user = user
        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = 'therapist'
        return token
    
class PatientTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user or not isinstance(user, CustomUser) or user.role != 'patient':
            raise serializers.ValidationError("Invalid credentials for Patient.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Attach the validated user to self.user as expected by super()
        self.user = user
        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email
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


class TherapistRegisterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Therapist
        fields = ['user', 'specialty', 'photo', 'working_hours', 'certificates', 'experience']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'therapist'
        user = CustomUser.objects.create_user(**user_data)
        therapist = Therapist.objects.create(user=user, **validated_data)
        return therapist


class PatientRegisterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'address', 'Birth_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'patient'
        user = CustomUser.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # reset_url = f"http://your-frontend-url.com/reset-password/{uid}/{token}/"

        # # Replace with real email settings
        # send_mail(
        #     subject="Reset your password",
        #     message=f"Click the link to reset your password: {reset_url}",
        #     from_email="no-reply@example.com",
        #     recipient_list=[email],
        # )