from rest_framework import serializers
from ..models.invoice import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'client', 'business', 'user', 'date', 'total_amount', 'service_cost', 'exam_cost', 'items']

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
        instance.save()

        # Clear existing items and add new ones
        instance.items.clear()
        total_amount = instance.service_cost + instance.exam_cost
        for item_data in items_data:
            item = InvoiceItem.objects.create(invoice=instance, **item_data)
            total_amount += item.price * item.quantity
        instance.total_amount = total_amount
        instance.save()

        return instance