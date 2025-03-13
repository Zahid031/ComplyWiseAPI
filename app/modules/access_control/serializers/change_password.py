from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    old_password=serializers.CharField(write_only=True,required=True)
    new_password=serializers.CharField(write_only=True, required=True)
    confirm_password=serializers.CharField(write_only=True, required=True)

