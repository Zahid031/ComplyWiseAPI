from rest_framework import viewsets

from ..models.roles import Role,UserRole,RolePermission
from ..models.menu import Menu
from ..serializers.roles import RoleSerializer,RolePermissionSerializer,MenuSerializer,UserRoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset =Menu.objects.all()
    serializer_class=MenuSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset=RolePermission.objects.all()
    serializer_class=RolePermissionSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset=UserRole.objects.all()
    serializer_class=UserRoleSerializer
    


