from rest_framework import viewsets
from ..models.business import Business
from ..serializers.business_serializer import BusinessSerializer

class BusinessCreateView(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = []  # Permitir acceso sin autenticación para registrar un negocio