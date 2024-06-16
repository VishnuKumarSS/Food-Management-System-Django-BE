from django.contrib.auth import get_user_model
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
    password = serializers.CharField(write_only=True) # So that it will not be returned to the user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Generate OTP and send email
        otp = generate_otp()
        OTP.objects.create(email=user.email, otp=otp)
        send_otp_email(user.email, otp)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    otp = serializers.CharField(write_only=True, required=False, max_length=6)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("JWT Token payload function triggered.")
        # Include these keys in the JWT data
        # uid is included by default as we mentioned 'USER_ID_FIELD': 'uid' in settings.
        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
    
        email = attrs.get('email')
        password = attrs.get('password')
        print('Validation Attibutes:', attrs)

        if email and password:
            user = self.get_user(email, password)
            
            if not user:
                raise serializers.ValidationError("User not found with the provided credentials.")
            
            print("User object:", user.__dict__)

            # Validate OTP, when the email is not verified
            if not user.is_email_verified:
                otp = attrs.get('otp')
                
                if not otp:
                    raise serializers.ValidationError('otp field required.')

                otp_record = OTP.objects.filter(email=email, otp=otp).first()
                if otp_record and otp_record.is_valid_otp():
                    user.is_email_verified = True
                    user.save()
                    otp_record.delete()
                else:
                    raise serializers.ValidationError('Invalid OTP or OTP has expired.')

            data = super().validate(attrs)
            
            data['email'] = user.email
            data['username'] = user.username
            data['user_id'] = user.uid
            
            return data
            
        else:
            raise serializers.ValidationError('email, password fields are required.')


    def get_user(self, email, password):
        user = None
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                return user
            
            # * Or we can directly use this to get the user object
            # from django.contrib.auth import authenticate
            # user = authenticate(username=email, password=password)
            # return user
        
        return None