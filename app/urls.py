from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.modules.access_control.views.employee import EmployeeViewSet
from app.modules.access_control.views.user import RegisterView, LoginView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

