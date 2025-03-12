# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import login, logout
# from django.core.mail import send_mail
# from ..models import User
# from ..serializers import LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, UserSerializer
# from ..services import AuthService



# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             access_token = AuthService.create_access_token(user, 'Your Application Name')
#             return Response({
#                 'access_token': access_token.token,
#                 'expires_in': access_token.expires
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         logout(request)
#         return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# class ChangePasswordView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if not user.check_password(serializer.validated_data["old_password"]):
#                 return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)

#             user.set_password(serializer.validated_data["new_password"])
#             user.save()
#             return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ForgotPasswordView(APIView):
#     def post(self, request):
#         serializer = ForgotPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             user = User.objects.filter(email=email).first()
#             if user:
#                 # Simulating email sending (replace with actual logic)
#                 send_mail("Password Reset Request", "Reset your password here.", "admin@example.com", [email])
#             return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)