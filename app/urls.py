from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.modules.access_control.views.employee import EmployeeViewSet
# from app.modules.access_control.views.user import RegisterView, LoginView
from app.modules.access_control.views.register import RegisterView
from app.modules.access_control.views.send_otp import SendOTPView
from app.modules.access_control.views.validate_otp import ValidateOTPView
from app.modules.auth.views.login import LoginView
from app.modules.access_control.views.change_password import ChangePasswordView
from app.modules.access_control.views.reset_password import ResetPasswordView
from app.modules.access_control.views.user_profile import UserProfileView
from app.modules.access_control.views.user import UserViewSet
from app.modules.access_control.views.roles import RoleViewSet, MenuViewSet, RolePermissionViewSet, UserRoleViewSet


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'users',UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'role-permissions',RolePermissionViewSet)
router.register(r'user-roles', UserRoleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("validate-otp/",ValidateOTPView.as_view(), name="validate-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("change-password/",ChangePasswordView.as_view(), name="change-password"),
    path("reset-password/",ResetPasswordView.as_view(), name="reset-password"),
    #path('user-profile/',UserProfileView.as_view(),name='user-profile'),


    #path("login/", LoginView.as_view(), name="login"),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

