from rest_framework import serializers
from ..models.invoice import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'inventory_item', 'quantity', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'client', 'business', 'user', 'date', 'total_amount', 'service_cost', 'exam_cost', 'items', 'appointment']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        business = user.business
        invoice = Invoice.objects.create(user=user, business=business, **validated_data)
        total_amount = validated_data.get('service_cost', 0) + validated_data.get('exam_cost', 0)
        for item_data in items_data:
            item = InvoiceItem.objects.create(invoice=invoice, **item_data)
            total_amount += item.price * item.quantity
        invoice.total_amount = total_amount
        invoice.save()
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.client = validated_data.get('client', instance.client)
        instance.service_cost = validated_data.get('service_cost', instance.service_cost)
        instance.exam_cost = validated_data.get('exam_cost', instance.exam_cost)
        instance.date = validated_data.get('date', instance.date)
        instance.appointment = validated_data.get('appointment', instance.appointment)
        instance.save()

        # Actualizar los items de la factura
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = InvoiceItem.objects.get(id=item_id, invoice=instance)
                item.inventory_item = item_data.get('inventory_item', item.inventory_item)
                item.quantity = item_data.get('quantity', item.quantity)
                item.price = item_data.get('price', item.price)
                item.save()
            else:
                InvoiceItem.objects.create(invoice=instance, **item_data)

        # Recalcular el total_amount
        total_amount = instance.service_cost + instance.exam_cost
        for item in instance.items.all():
            total_amount += item.price * item.quantity
        instance.total_amount = total_amount
        instance.save()

        return instance