from rest_framework import serializers
from django.contrib.auth import authenticate
#from app.models import User
from django.contrib.auth import get_user_model

User=get_user_model()




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # def validate(self, data):
    #     user=authenticate(email=data['email'],password=data['password'])
    #     if not user:
    #         raise serializers.ValidationError("Invalid crefindials")
    #     if not user.email_verified:
    #         raise serializers.ValidationError("Email is not verified")
    #     return user
    