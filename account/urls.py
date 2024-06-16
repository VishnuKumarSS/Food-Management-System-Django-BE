from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CustomTokenObtainPairView, RegisterView, RequestOTP,
                    UserDetailView, VerifyOTP)

urlpatterns = [
    path('request-otp/', RequestOTP.as_view(), name='request_otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/userdata/', UserDetailView.as_view(), name='user_detail'),
]
