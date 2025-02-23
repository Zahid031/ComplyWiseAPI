from rest_framework import serializers
from .models import CustomUser
from .utils import generate_otp, send_otp_email
from django.utils import timezone

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        otp = generate_otp()
        user.otp = otp
        user.otp_exp = timezone.now() + timezone.timedelta(minutes=10)
        user.save()
        send_otp_email(user.email, otp)
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        otp = data['otp']
        try:
            user = CustomUser.objects.get(email=email)
            if user.otp != otp or user.otp_exp < timezone.now():
                raise serializers.ValidationError("Invalid OTP or OTP expired.")
            user.is_email_verified = True
            user.otp = None
            user.otp_exp = None
            user.save()
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.is_email_verified:
                raise serializers.ValidationError("Please verify your email first.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid credentials.")
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
            otp = generate_otp()
            user.otp = otp
            user.otp_exp = timezone.now() + timezone.timedelta(minutes=10)
            user.save()
            send_otp_email(user.email, otp)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        otp = data['otp']
        try:
            user = CustomUser.objects.get(email=email)
            if user.otp != otp or user.otp_exp < timezone.now():
                raise serializers.ValidationError("Invalid OTP or OTP expired.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return data

    def create(self, validated_data):
        email = validated_data['email']
        new_password = validated_data['new_password']
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.otp = None
            user.otp_exp = None
            user.save()
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return user