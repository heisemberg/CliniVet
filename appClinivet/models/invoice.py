from django.db import models
from .client import Client
from .inventory_item import InventoryItem

class Invoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='invoices', on_delete=models.CASCADE)
    date = models.DateTimeField('Date', auto_now_add=True)
    total_amount = models.DecimalField('Total Amount', max_digits=10, decimal_places=2)
    items = models.ManyToManyField(InventoryItem, through='InvoiceItem')

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)