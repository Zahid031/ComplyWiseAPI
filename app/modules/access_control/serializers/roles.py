from rest_framework import serializers
from ..models.roles import Role,RolePermission,UserRole
from ..models.menu import Menu
from app.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'

# class RolePermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RolePermission
#         fields = ["menu", "can_create", "can_read", "can_update", "can_delete","can_reports","list_view"] 
#         #fields = '__all__' 

#     def create(self, validated_data):
#         role = self.context["role"]  
#         return RolePermission.objects.create(role=role, **validated_data)


# class RoleSerializer(serializers.ModelSerializer):
#     permissions = RolePermissionSerializer(many=True)  

#     class Meta:
#         model = Role
#         fields = ["id", "name", "permissions"]

#     def create(self, validated_data):
#         permissions_data = validated_data.pop("permissions", []) 
#         role = Role.objects.create(**validated_data) 
#         for perm_data in permissions_data:
#             RolePermission.objects.create(role=role, **perm_data)
#         return role
    
#     def update(self, instance, validated_data):
#         permissions_data = validated_data.pop("permissions", [])  # Extract permissions data
#         instance.name = validated_data.get("name", instance.name)  # Update role name if changed
#         instance.save()

#         # Existing permissions mapped by menu ID
#         existing_permissions = {perm.menu.id: perm for perm in instance.permissions.all()}

#         new_permissions = []  # Track new permission instances
#         updated_menus = set()  # Track updated menus to remove unused permissions later

#         for perm_data in permissions_data:
#             menu_id = perm_data.get("menu")
#             if menu_id in existing_permissions:
#                 # Update existing permission
#                 perm_instance = existing_permissions[menu_id]
#                 for attr, value in perm_data.items():
#                     setattr(perm_instance, attr, value)
#                 perm_instance.save()
#                 updated_menus.add(menu_id)
#             else:
#                 # Create new permission
#                 new_permissions.append(RolePermission(role=instance, **perm_data))

#         # Bulk create new permissions
#         if new_permissions:
#             RolePermission.objects.bulk_create(new_permissions)

#         # Remove permissions not included in the update request
#         RolePermission.objects.filter(role=instance).exclude(menu_id__in=updated_menus).delete()

#         return instance


#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['permissions'] = RolePermissionSerializer(instance.permissions.all(), many=True).data
#         return response


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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["permissions"] = RolePermissionSerializer(instance.permissions.all(), many=True).data
        return response


class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model=UserRole
        fields=['id','user','role']



