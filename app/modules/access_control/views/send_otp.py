from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import User
from ..serializers.send_otp import SendOTPSerializer
import random
from app.modules.access_control.models.otp import OTP
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
import datetime
from django.conf import settings as SETTINGS

from rest_framework.generics import CreateAPIView


# class SendOTPView(APIView):
#     #serializer_class = SendOTPSerializer
    
#     def post(self,request, *args, **kwargs):
#         serializer=SendOTPSerializer(data=request.data)

#         if serializer.is_valid():
#             email=serializer.validated_data['email']
#             user=User.objects.get(email=email)
#             otp_code=f'{random.randint(100000,999999)}'
#             otp_instance=OTP.objects.create(
#                 user=user,
#                 otp_code=otp_code,
#                 expires_at=timezone.now() + timedelta(minutes=10)
#                 )
#             send_mail(
#                 subject='OTP Verification',
#                 message=f'Your OTP is {otp_code}',
#                 from_email=SETTINGS.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.email],
#                 fail_silently=False,

#             )
#             return Response({'message':'OTP sent successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SendOTPView(CreateAPIView):
    serializer_class= SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(100000, 999999))
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        OTP.objects.create(user=user, otp_code=otp_code, expires_at=otp_expiry)

        send_mail(
            subject='OTP Verification',
            message=f'Your OTP is {otp_code}',
            from_email=SETTINGS.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            )

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
        
