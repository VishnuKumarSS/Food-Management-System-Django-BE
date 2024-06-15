from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTP, User
from .serializers import OTPRequestSerializer, OTPVerifySerializer
from .utils import generate_otp, send_otp_email


class RequestOTP(APIView):

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = generate_otp()
            OTP.objects.create(email=email, otp=otp)
            send_otp_email(email, otp)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            otp_record = OTP.objects.filter(email=email, otp=otp).first()
            
            if otp_record and otp_record.is_valid_otp():
                user = User.objects.filter(email=email).first()
                if user:
                    user.is_email_verified = True  # Mark email as verified
                    user.save()
                otp_record.delete()
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        
            return Response({'error': 'Invalid OTP or OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
