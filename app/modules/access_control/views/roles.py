from rest_framework import viewsets, status
from ..models.roles import Role,UserRole
from ..models.menu import Menu
from ..serializers.roles import RoleSerializer,MenuSerializer,UserRoleSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from app.permissions import RoleBasedPermission

class MenuViewSet(viewsets.ModelViewSet):
    queryset =Menu.objects.all()
    serializer_class=MenuSerializer
    #permission_classes =[RoleBasedPermission]
            

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():  
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            role = serializer.save()
            return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset=UserRole.objects.all()
    serializer_class=UserRoleSerializer
    


