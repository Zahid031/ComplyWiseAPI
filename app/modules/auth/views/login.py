from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.login  import LoginSerializer
from django.contrib.auth import authenticate
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken,RefreshToken
from oauthlib.common import generate_token
from oauth2_provider.settings import oauth2_settings
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from django.utils.timezone import now



class LoginView(CreateAPIView):
    permission_classes=[]

    serializer_class=LoginSerializer
    def post(self,request):
        serializers=LoginSerializer(data=request.data)
        if serializers.is_valid():
            email=serializers.validated_data['email']
            password=serializers.validated_data['password']
            user=authenticate(request,email=email,password=password)
            if not user:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                raise serializers.ValidationError("Email is not verified")
            try:
                app=Application.objects.get(client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type="password")
            except Application.DoesNotExist:
                return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
            access_token=AccessToken.objects.create(
                user=user,
                token=generate_token(),
                application=app,
                scope='read write',
                expires=now()+timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            )
            return Response({
            'access_token': access_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            #'refresh_token': refresh_token.token,
            'token_type': 'Bearer'
            },status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            


