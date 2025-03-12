from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.validate_otp import ValidateOTPSerializer
from app.models import User
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import CreateAPIView



class ValidateOTPView(CreateAPIView):
    serializer_class = ValidateOTPSerializer

    def post(self, request):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])
        user.email_verified_at = now()
        user.is_active = True
        user.save()

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)