from rest_framework import serializers
from app.models import User
from app.modules.access_control.models.otp import OTP


class ValidateOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError("User does not exist")

        otp_instance = OTP.objects.filter(user=user, otp_code=data['otp']).first()
        if not otp_instance or not otp_instance.is_valid():
            raise serializers.ValidationError("Invalid or expired OTP")

        return data