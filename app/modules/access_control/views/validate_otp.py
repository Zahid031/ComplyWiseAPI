from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.validate_otp import ValidateOTPSerializer
from app.models import User
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import CreateAPIView
from app.models import User
from app.modules.access_control.models.otp import OTP
from rest_framework.generics import GenericAPIView

class ValidateOTPView(GenericAPIView):
    permission_classes=[]
    serializer_class = ValidateOTPSerializer

    def post(self, request):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data['email']
        otp_code=serializer.validated_data['otp_code']

        try:
            user=User.objects.get(email=email)
            otp_instance=OTP.objects.get(user=user, otp_code=otp_code)
            if not otp_instance.is_valid():
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_otp_verified= True
            user.is_active = True
            user.email_verified_at = now()
            user.save()
            otp_instance.delete()
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


        except (User.DoesNotExist,OTP.DoesNotExist):
            return Response({"error": "Invalid email or OTP"}, status=status.HTTP_400_BAD_REQUEST)


        # user = User.objects.get(email=serializer.validated_data['email'])
        # user.email_verified_at = now()
        # user.is_active = True
        # user.save()

        # return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        
