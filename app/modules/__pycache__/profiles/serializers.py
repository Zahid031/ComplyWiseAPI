from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=['id','user','first_name','last_name','phone_number','address','created_at','updated_at']
        read_only_fields=['created_at','updated_at']

        