from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Include these keys in the JWT data
        # uid is included by default as we mentioned 'USER_ID_FIELD': 'uid' in settings.
        token['username'] = user.username
        token['email'] = user.email

        return token
