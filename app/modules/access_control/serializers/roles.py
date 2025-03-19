from rest_framework import serializers

from ..models.roles import Role,RolePermission,UserRole
from ..models.menu import Menu
from app.models import User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    role_name=serializers.CharField(source='role.name',read_only=True)
    menu_name=serializers.CharField(source='menu.name',read_only=True)

    class Meta:
        model=RolePermission
        fields='__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model=UserRole
        fields=['id','user','role']



