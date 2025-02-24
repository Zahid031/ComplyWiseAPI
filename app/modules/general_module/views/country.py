from rest_framework import viewsets
from ..models.country import Country
from ..serializers.country import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer