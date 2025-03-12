from rest_framework import serializers
from django.contrib.auth import authenticate
from app.models import User

class UserRegistrationSerializer(serializers.ModelSerializer): 
    #password = serializers.CharField(write_only=True)   
    class Meta:
        model = User
        fields = ["email","full_name","mobile_no", "password"]
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            full_name=validated_data["full_name"],
            mobile_no=validated_data["mobile_no"],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    

