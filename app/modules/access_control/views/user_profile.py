from rest_framework import generics,permissions
from rest_framework.response import Response
from ..serializers.user_profile import ProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
    