# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate

# User = get_user_model()

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")
    
# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         if data["new_password"] != data["confirm_password"]:
#             raise serializers.ValidationError("Passwords do not match")
#         return data

# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()