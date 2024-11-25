from rest_framework import serializers
from ..models.inventory_item import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'category', 'description', 'price', 'quantity']