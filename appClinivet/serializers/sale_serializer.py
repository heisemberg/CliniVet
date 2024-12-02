from rest_framework import serializers
from ..models.sale import Sale, SaleItem
from ..models.inventory_item import InventoryItem
from ..models.invoice import Invoice

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['inventory_item', 'quantity', 'price']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'business', 'date', 'total_amount', 'items', 'invoice']
        read_only_fields = ['date', 'total_amount', 'invoice']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        total_amount = 0

        for item_data in items_data:
            inventory_item = item_data['inventory_item']
            quantity = item_data['quantity']
            price = item_data['price']

            # Validar la cantidad disponible en el inventario
            if inventory_item.quantity < quantity:
                raise serializers.ValidationError(f"Not enough quantity for item {inventory_item.name}. Available: {inventory_item.quantity}, requested: {quantity}")

            # Crear el SaleItem
            SaleItem.objects.create(sale=sale, inventory_item=inventory_item, quantity=quantity, price=price)

            # Actualizar el inventario
            inventory_item.quantity -= quantity
            inventory_item.save()

            total_amount += price * quantity

        sale.total_amount = total_amount
        sale.save()

        # Generar la factura automáticamente
        invoice = Invoice.objects.create(
            amount=total_amount,
            date=sale.date,
            sale=sale,
            business=sale.business,
            client=sale.client
        )
        sale.invoice = invoice
        sale.save()

        return sale