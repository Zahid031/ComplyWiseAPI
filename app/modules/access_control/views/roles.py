from rest_framework import viewsets, status
from ..models.roles import Role,UserRole,RolePermission
from ..models.menu import Menu
from ..serializers.roles import RoleSerializer,MenuSerializer,UserRoleSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from app.permissions import RoleBasedPermission
from app.models import User
from rest_framework.views import APIView
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast



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
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        role_ids = request.data.get('roles') #or request.data.get('role')

        if not isinstance(role_ids, list):
            return Response({'error': 'Roles should be a list'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with ID {user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        created_roles = []

        for role_id in role_ids:
            try:
                role = Role.objects.get(pk=role_id)
                user_role, created = UserRole.objects.get_or_create(user=user, role=role)
                if created:
                    created_roles.append(user_role)
            except Role.DoesNotExist:
                return Response({'error': f'Role with ID {role_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(created_roles, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCombinedPermissionView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        role_ids = UserRole.objects.filter(user=user).values_list('role', flat=True)

        permissions = (
            RolePermission.objects
            .filter(role_id__in=role_ids)
            .values('menu_id')
            .annotate(
                can_read=Max(Cast('can_read', IntegerField())),
                can_create=Max(Cast('can_create', IntegerField())),
                can_update=Max(Cast('can_update', IntegerField())),
                can_delete=Max(Cast('can_delete', IntegerField())),
                can_reports=Max(Cast('can_reports', IntegerField())),
                list_view=Max(Cast('list_view', IntegerField()))
            )
        )

        result = {
            "user_id": user.id,
            "permissions": []
        }

        for perm in permissions:
            #menu = Menu.objects.get(id=perm['menu_id'])
            result['permissions'].append({
                "menu_id": perm["menu_id"],#MenuSerializer(menu).data,
                "can_create": bool(perm['can_create']),
                "can_read": bool(perm['can_read']),
                "can_update": bool(perm['can_update']),
                "can_delete": bool(perm['can_delete']),
                "can_reports": bool(perm['can_reports']),
                "list_view": bool(perm['list_view']),
            })

        return Response(result, status=status.HTTP_200_OK)