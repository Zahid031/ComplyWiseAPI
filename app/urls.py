from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.modules.access_control.views.employee import EmployeeViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

