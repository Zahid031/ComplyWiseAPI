from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.reset_password import ResetPasswordSerializer
from app.models import User
from rest_framework import status

class ResetPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
           # print(f"User: {user.email}, OTP Verified: {user.is_otp_verified}")  
            
            if not user.is_otp_verified:
                return Response({"error": "OTP not verified. Please verify the OTP first."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.is_otp_verified = False  
            user.save()
            
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)