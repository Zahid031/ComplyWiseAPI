from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .modules.access_control.views.ev_user import EVUserViewSet
from .modules.general_module.views.country import CountryViewSet

from .modules.station_management.views.charging_port import ChargingPortViewSet
from .modules.station_management.views.charging_scope import ChargingScopeViewSet
from .modules.station_management.views.charging_station import ChargingStationViewSet

from .modules.vehicle_management.views.ev_battery_type import EVBatteryTypeViewSet
from .modules.vehicle_management.views.ev_charging_port_type import EVChargingPortTypeViewSet
from .modules.vehicle_management.views.ev_drivetrain import EVDrivetrainViewSet
from .modules.vehicle_management.views.ev_manufacturer import EVManufacturerViewSet
from .modules.vehicle_management.views.ev_model import EVModelViewSet
from .modules.vehicle_management.views.ev_thermalsystem import EVThermalSystemViewSet
from .modules.vehicle_management.views.ev_type import EVTypeViewSet
from .modules.vehicle_management.views.evehicle import EVehicleViewSet
from .modules.vehicle_management.views.users_ev import UsersEVViewSet

from .modules.wallet.views.users_payment_method import UsersPaymentMethodViewSet
from .modules.wallet.views.users_wallet import UsersWalletViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()

router.register(r'ev-users', EVUserViewSet)
router.register(r'countries', CountryViewSet)

router.register(r'charging-ports', ChargingPortViewSet)
router.register(r'charging-scopes', ChargingScopeViewSet)
router.register(r'charging-stations', ChargingStationViewSet)

router.register(r'ev-battery-types', EVBatteryTypeViewSet)
router.register(r'ev-charging-port-types', EVChargingPortTypeViewSet)
router.register(r'ev-drivetrains', EVDrivetrainViewSet)
router.register(r'ev-manufacturers', EVManufacturerViewSet)
router.register(r'ev-models', EVModelViewSet)
router.register(r'ev-thermal-systems', EVThermalSystemViewSet)
router.register(r'ev-types', EVTypeViewSet)
router.register(r'evehicles', EVehicleViewSet)
router.register(r'users-ev', UsersEVViewSet)

router.register(r'users-payment-methods', UsersPaymentMethodViewSet)
router.register(r'users-wallets', UsersWalletViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

