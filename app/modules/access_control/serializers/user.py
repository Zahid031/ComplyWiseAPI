# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from ..models.user import User

# class UserRegistrationSerializer(serializers.ModelSerializer): 
#     password = serializers.CharField(write_only=True)   
#     class Meta:
#         model = User
#         fields = ["email", "password"]
#         extra_kwargs = {"password": {"write_only": True}}
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     # class Meta:
#     #     model = User
#     #     fields = ['email', 'password']

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#         fields = ['email', 'password']
        
#         if email and password:
#             user = authenticate(email=email, password=password)
#             if user:
#                 return {'user': user}
#         raise serializers.ValidationError("Invalid email or password")
    
