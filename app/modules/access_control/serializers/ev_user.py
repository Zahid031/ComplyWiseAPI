from rest_framework import serializers
from ..models.ev_user import EVUser

class EVUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVUser
        fields = '__all__'