from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.sale import Sale
from ..serializers.sale_serializer import SaleSerializer
from ..permissions import IsDoctorOrSellerOrAdmin

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrSellerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(business=user.business)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)