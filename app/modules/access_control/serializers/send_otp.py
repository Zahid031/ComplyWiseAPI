from rest_framework import serializers
from app.models import User
from app.modules.access_control.models.otp import OTP


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

