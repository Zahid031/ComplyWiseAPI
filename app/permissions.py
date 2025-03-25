from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from app.modules.access_control.models.roles import UserRole, RolePermission
from app.modules.access_control.models.menu import Menu

class RoleBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        print(user)
        
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        
        menu = Menu.objects.filter(url__icontains=request.path).first()
        #print(request.path)
        
        if not menu:

            raise PermissionDenied(f"Menu not found for URL: {request.path}")

        user_role = UserRole.objects.filter(user=user).select_related('role').first()
        if not user_role:
            raise PermissionDenied("User role not assigned.")

        permission = RolePermission.objects.filter(role=user_role.role, menu=menu).first()
        if not permission:
            raise PermissionDenied("Permission not assigned to this menu.")
        
        method_permission_map = {
            'GET': 'can_read',
            'POST': 'can_create',
            'PUT': 'can_update',
            'PATCH': 'can_update',
            'DELETE': 'can_delete',
        }

        permission_attr = method_permission_map.get(request.method)
        if permission_attr and not getattr(permission, permission_attr, False):
            raise PermissionDenied(f"You do not have permission to {request.method.lower()}.")

        if request.method == "GET":
            if hasattr(permission, "list_view") and not permission.list_view:
                raise PermissionDenied("You do not have permission to view the list.")
            if hasattr(permission, "can_reports") and not permission.can_reports:
                raise PermissionDenied("You do not have permission to view reports.")

        return True
