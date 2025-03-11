from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.timezone import now
from ..serializers.user import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate,get_user_model,authenticate
from rest_framework import status
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from datetime import timedelta
from oauthlib.common import generate_token


User = get_user_model()

class RegisterView(APIView):
    serializer_class= UserRegistrationSerializer
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)
            if not user:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                app=Application.objects.get(client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type="password")
            except Application.DoesNotExist:
                return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
            # print(app)
            access_token=AccessToken.objects.create(
                user=user,
                token=generate_token(),
                application=app,
                expires=now()+timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
                scope="read write"
            )
            refresh_token=RefreshToken.objects.create(
                user=user,
                token=generate_token(),
                application=app,
                access_token=access_token,
                #expires=now()+timedelta(seconds=oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS)

            )
            return Response({
                'access_token': access_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'refresh_token': refresh_token.token,

                'token_type': 'Bearer'
            },status=status.HTTP_200_OK)
        
              






















# from rest_framework import viewsets, status, generics, views
# from rest_framework.decorators import action
# from rest_framework.views import APIView

# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from oauth2_provider.models import Application, AccessToken, RefreshToken
# from django.utils import timezone
# from datetime import timedelta
# from oauthlib.oauth2 import BackendApplicationClient
# from requests_oauthlib import OAuth2Session
# from oauthlib.common import generate_token
# from ..models.user import User
# from ..serializers.user import UserRegistrationSerializer, UserLoginSerializer
# from django.contrib.auth import get_user_model,login
# import requests

# User = get_user_model()

# class RegisterViewset(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"message": "User registered successfully!"}, 
#             status=status.HTTP_201_CREATED
#         )


# class LoginView(APIView):
#     serializer_class = UserLoginSerializer
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             #user=serializer.validated_data['user']
#             email=serializer.validated_data['email']
#             password=serializer.validated_data['password']
#             payload= {
#                 'grant_type': 'password',
#                 'username': email,
#                 'password': password,
#                 'client_id': 'L0hvTXXGxb5YT41NwMEXC5cGpuFS747QFdKofeCP',
#                 'client_secret': 'AZbekHhyUIAwKYUSWTYQjc072QZ6O2Q37sqIYlt8cx8gePRECaosuJyl95GoavfX4dwNcxBcvQPXaaBdktfWtmXjNL2XdCrWiVLIg89onElMxoceBUyTxAeJkZm9lRii'
#             }
#             token_url=f"{request.scheme}://{request.get_host()}/o/token/"
#             response = requests.post(token_url, data=payload)  
#             if response.status_code==200:
#                 token_data=response.json()
#                 return Response({
#                     'message': 'Login successful',
#                     'access_token': token_data['access_token'],
#                     'refresh_token': token_data['refresh_token'],
#                     'expires_in': token_data['expires_in'],
#                 },status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
            
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        





# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
    
#     def _get_default_application(self, user):
#         app, created = Application.objects.get_or_create(
#             user=user,
#             defaults={
#                 'name': 'Default',
#                 'client_type': Application.CLIENT_CONFIDENTIAL,
#                 'authorization_grant_type': Application.GRANT_PASSWORD,
#                 'skip_authorization': True
#             }
#         )
#         return app
    
#     def _create_tokens(self, user, application):
#         # Create access token
#         expires = timezone.now() + timedelta(days=1)
#         access_token = AccessToken.objects.create(
#             user=user,
#             application=application,
#             token=generate_token(),
#             expires=expires,
#             scope='read write'
#         )
        
#         refresh_token = RefreshToken.objects.create(
#             user=user,
#             application=application,
#             token=generate_token(),
#             access_token=access_token
#         )
        
#         return {
#             'access_token': access_token.token,
#             'refresh_token': refresh_token.token,
#             'expires_in': 86400,  # 1 day in seconds
#             'token_type': 'Bearer',
#             'scope': access_token.scope
#         }
    
#     @action(detail=False, methods=['post'], url_path='register')
#     def register(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             application = self._get_default_application(user)
#             tokens = self._create_tokens(user, application)
            
#             return Response({
#                 "message": "Registration successful",
#                 "email": user.email,
#                 **tokens
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @action(detail=False, methods=['post'], url_path='login')
#     def login(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             application = self._get_default_application(user)
#             tokens = self._create_tokens(user, application)
            
#             return Response({
#                 "message": "Login successful",
#                 "email": user.email,
#                 **tokens
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)