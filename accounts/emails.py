from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser

def send_otp_via_email(email):
    subject = "Your account verification email"
    otp = random.randint(1000,9999)
    message = f"Hello,\n\n" \
              f"Thank you for registering with our service. To verify your account, please use the following One-Time Password (OTP):\n\n" \
              f"OTP: {otp}\n\n" \
              f"This OTP is valid for a single use and will expire in 10 minutes. Please enter this OTP on the verification page to activate your account.\n\n" \
              f"If you didn't request this OTP, please disregard this email and contact our support team immediately.\n\n" \
              f"Best regards,\n" \
              f"TherapEase Team"
    email_from = settings.EMAIL_HOST
    # send_mail(subject,message,email_from, [email])
    try:
        send_mail(subject, message, email_from, [email])
    except Exception as e:
        # Handle the exception, e.g., by printing the error message
        print(f"An error occurred while sending the email: {e}")
    user_obj = CustomUser.objects.get(email= email)
    user_obj.otp = otp
    user_obj.save()