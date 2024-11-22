"""
URL configuration for projectClinivet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from appClinivet.views.user_view import UserCreateView
from appClinivet.views.pet_view import PetViewSet
from appClinivet.views.medical_record_view import MedicalRecordViewSet
from appClinivet.views.appointment_view import AppointmentViewSet
from appClinivet.views.availability_view import AvailabilityViewSet
from appClinivet.views.inventory_item_view import InventoryItemViewSet
from appClinivet.views.invoice_view import InvoiceViewSet

# Crear el router y registrar las vistas
router = DefaultRouter()
router.register(r'users', UserCreateView)
router.register(r'pets', PetViewSet)
router.register(r'medical_records', MedicalRecordViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'inventory_items', InventoryItemViewSet)
router.register(r'invoices', InvoiceViewSet)

# Definir las rutas específicas y las rutas generadas por el router
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]