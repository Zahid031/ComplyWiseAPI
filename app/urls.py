from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.modules.access_control.views.employee import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

