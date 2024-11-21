from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.invoice import Invoice
from ..serializers.invoice_serializer import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]