from rest_framework import serializers
from ..models.sale import Sale, SaleItem
from ..models.invoice import Invoice

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'business', 'date', 'total_amount', 'items', 'invoice']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice_data = validated_data.pop('invoice', None)
        sale = Sale.objects.create(**validated_data)
        total_amount = 0
        for item_data in items_data:
            item = SaleItem.objects.create(sale=sale, **item_data)
            total_amount += item.price * item.quantity
        sale.total_amount = total_amount
        sale.save()

        if invoice_data:
            invoice = Invoice.objects.create(**invoice_data, user=self.context['request'].user, business=sale.business)
            sale.invoice = invoice
            sale.save()

        return sale