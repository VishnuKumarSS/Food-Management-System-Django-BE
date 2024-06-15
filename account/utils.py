import random

from django.conf import settings
from django.core.mail import send_mail


def generate_otp(length=6):
    """
    Generates 6 digit OTP
    """
    return ''.join(random.choices('0123456789', k=length))


def send_otp_email(email, otp):
    """
    Utility function that sends OTP to the specified email address.
    """
    subject = 'Food Management System - OTP Code'
    message = (
        f"<div >"
        f"<h2>Food Management System</h2>"
        f"<p>Your OTP code is <span style='color: #4CAF50; font-weight: bold;'>{otp}</span>. It will expire in 5 minutes.</p>"
        f"</div>"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        html_message=message
    )
