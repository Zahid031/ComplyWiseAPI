from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from app.models import User

from ..serializers.change_password import ChangePasswordSerializer
#User=get_user_model()


class ChangePasswordView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class=ChangePasswordSerializer
    #@swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            old_password=serializer.validated_data['old_password']
            new_password=serializer.validated_data['new_password']
            confirm_password=serializer.validated_data['confirm_password']
            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)
            if not user.check_password(old_password):
                return Response({"error":"Invalid Old Password"},status=status.HTTP_400_BAD_REQUEST)
            if new_password!=confirm_password:
                return Response({"error":"New Password and Confirm Password do not macth"},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message":"Password Changed Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

