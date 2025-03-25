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
        fields = ["menu", "can_create", "can_read", "can_update", "can_delete", "can_reports", "list_view"]

    def validate_menu(self, value):
        if not Menu.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid menu ID.")
        return value

class RoleSerializer(serializers.ModelSerializer):
    permissions = RolePermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        permissions_data = validated_data.pop("permissions", [])
        role = Role.objects.create(**validated_data)

        for perm_data in permissions_data:
            menu_id = perm_data.pop("menu").id 
            menu = Menu.objects.get(id=menu_id)  
            RolePermission.objects.create(role=role, menu=menu, **perm_data)

        return role

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop("permissions", [])
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        existing_permissions = {perm.menu.id: perm for perm in instance.permissions.all()}
        updated_menus = set()

        for perm_data in permissions_data:
            menu_id = perm_data.pop("menu").id 
            updated_menus.add(menu_id)

            if menu_id in existing_permissions:
                perm_instance = existing_permissions[menu_id]
                for attr, value in perm_data.items():
                    setattr(perm_instance, attr, value)
                perm_instance.save()
            else:
                menu = Menu.objects.get(id=menu_id)
                RolePermission.objects.create(role=instance, menu=menu, **perm_data)

        RolePermission.objects.filter(role=instance).exclude(menu_id__in=updated_menus).delete()
        return instance


class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model=UserRole
        fields=['id','user','role']



