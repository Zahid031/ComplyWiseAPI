from rest_framework import serializers
from ..models.roles import Role,RolePermission,UserRole
from ..models.menu import Menu
from app.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ["menu", "can_create", "can_read", "can_update", "can_delete","can_reports","list_view"] 
        #fields = '__all__' 

    def create(self, validated_data):
        role = self.context["role"]  
        return RolePermission.objects.create(role=role, **validated_data)


class RoleSerializer(serializers.ModelSerializer):
    permissions = RolePermissionSerializer(many=True)  

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        permissions_data = validated_data.pop("permissions", []) 
        role = Role.objects.create(**validated_data) 
        for perm_data in permissions_data:
            RolePermission.objects.create(role=role, **perm_data)
        return role


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['permissions'] = RolePermissionSerializer(instance.permissions.all(), many=True).data
        return response


class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model=UserRole
        fields=['id','user','role']



