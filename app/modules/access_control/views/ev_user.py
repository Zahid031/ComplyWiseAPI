from rest_framework import viewsets
from ..models.ev_user import EVUser
from ..serializers.ev_user import EVUserSerializer

class EVUserViewSet(viewsets.ModelViewSet):
    queryset = EVUser.objects.all()
    serializer_class = EVUserSerializer