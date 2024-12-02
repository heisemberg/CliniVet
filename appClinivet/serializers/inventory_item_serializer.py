from rest_framework import serializers
from ..models.inventory_item import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'product_code', 'name', 'category', 'description', 'price', 'quantity']

    def validate_product_code(self, value):
        request = self.context.get('request')
        business = request.user.business
        if InventoryItem.objects.filter(business=business, product_code=value).exists():
            raise serializers.ValidationError("Inventory item with this Product Code already exists within this business.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        business = request.user.business
        return InventoryItem.objects.create(business=business, **validated_data)