from rest_framework import serializers

from app.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["id","email","created_at","updated_at","full_name","mobile_no"]
        read_only_fields = ('id','email')
        #extra_kwargs = {'password': {'write_only': True}}
