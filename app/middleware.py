from django.utils.deprecation import MiddlewareMixin
from app.modules.access_control.models.roles import UserRole,RolePermission
from app.modules.access_control.models.menu import Menu
from django.http import JsonResponse

class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/api/') or request.path.startswith('/swagger/'):
            return None
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Authentication required"},status=401)
        menu=Menu.objects.filter(url=request.path).first()
        if not menu:
            return JsonResponse({"error":"Url not found"}, status=404)
        try:
            role=UserRole.objects.get(user=user)
        except UserRole.DoesNotExist:
            return JsonResponse({"error": "User role not assigned"},status=403)
        try:
            permission=RolePermission.objects.get(role=role.role,menu=menu)
        except RolePermission.DoesNotExist:
            return JsonResponse({"error":"Permission not assigned to this menu"},status=403)
        

        method_permission_map= {
            'GET': 'can_read',
            'POST': 'can_create',
            'PUT': 'can_update',
            'DELETE': 'can_delete',
        }
        if request.method in method_permission_map:
            if not getattr(permission, method_permission_map[request.method]):
                return JsonResponse({"error": "You do not have permission to perform this action."}, status=403)
            return JsonResponse({"error": "You do not have permission to create."}, status=403)
        
        if request.method == 'GET' and not permission.can_read:
            return JsonResponse({"error": "You do not have permission to read."}, status=403)
        
        if request.method == 'PUT' and not permission.can_update:
            return JsonResponse({"error": "You do not have permission to update."}, status=403)
        
        if request.method == 'DELETE' and not permission.can_delete:

            return JsonResponse({"error": "You do not have permission to delete."}, status=403)
        if request.method == 'GET' and not permission.list_view:
            return JsonResponse({"error": "You do not have permission to view list."}, status=403)
        if request.method == 'GET' and permission.can_reports:
            return JsonResponse({"error": "You do not have permission to view reports."}, status=403)
        
        return None
        