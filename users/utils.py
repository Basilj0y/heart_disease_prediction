# your_app/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user_email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [user_email])
