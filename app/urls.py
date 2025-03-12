from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.modules.access_control.views.employee import EmployeeViewSet
# from app.modules.access_control.views.user import RegisterView, LoginView
from app.modules.access_control.views.register import RegisterView
from app.modules.access_control.views.send_otp import SendOTPView
from app.modules.access_control.views.validate_otp import ValidateOTPView
from app.modules.auth.views.login import LoginView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("validate-otp/",ValidateOTPView.as_view(), name="validate-otp"),
    path("login/", LoginView.as_view(), name="login")
    #path("login/", LoginView.as_view(), name="login"),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

