from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.inventory_item import InventoryItem
from ..serializers.inventory_item_serializer import InventoryItemSerializer
from ..permissions import IsAdminOrReadOnly

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

