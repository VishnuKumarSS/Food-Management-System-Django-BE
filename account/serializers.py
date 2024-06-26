from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import OTP
from .utils import generate_otp, send_otp_email

User = get_user_model()


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uid', 'username', 'email', 'is_email_verified', 'is_admin', \
            'is_superuser', 'is_active', 'created_at', 'updated_at'
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # So that it will not be returned in the reponse

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    otp = serializers.CharField(write_only=True, required=False, max_length=6, allow_blank=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Include these keys in the JWT data
        # uid is included by default as we mentioned 'USER_ID_FIELD': 'uid' in settings.
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['is_superuser'] = user.is_superuser
        token['is_email_verified'] = user.is_email_verified

        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print('Validation Attibutes:', attrs)
        
        if not email or not password:
            raise serializers.ValidationError({'error': 'email and password fields are required.'})
        
        # Authenticate user
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise serializers.ValidationError({'error': 'User not found with the provided credentials.'})
        
        print("User object:", user.__dict__)

        # Validate OTP if email is not verified
        if not user.is_email_verified:
            otp = attrs.get('otp')
            if not otp:
                raise serializers.ValidationError({'error': 'otp field is required for unverified email.'})

            otp_record = OTP.objects.filter(email=email, otp=otp).first()
            if otp_record and otp_record.is_valid_otp():
                user.is_email_verified = True
                user.save()
                otp_record.delete()
            else:
                raise serializers.ValidationError({'error': 'Invalid OTP or OTP has expired.'})

        data = super().validate(attrs)
        
        # Add the required fields to be included in the response in addition to the access token and refresh token.
        data.update({
            'email': user.email,
            'username': user.username,
            'user_id': user.uid
        })
        
        return data
