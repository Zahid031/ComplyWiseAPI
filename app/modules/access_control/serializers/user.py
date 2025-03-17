from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields=["id","created_at","updated_at","email","full_name","mobile_no","password"]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop("password")  
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password", None)  
        return super().update(instance, validated_data)
       
