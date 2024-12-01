from rest_framework import serializers
from ..models.inventory_item import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'product_code', 'name', 'category', 'description', 'price', 'quantity', 'business']
        read_only_fields = ['business']

    def create(self, validated_data):
        request = self.context.get('request')
        business = request.user.business
        return InventoryItem.objects.create(business=business, **validated_data)