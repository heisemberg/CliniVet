from django.db import models
from .client import Client
from .inventory_item import InventoryItem
from .business import Business
from .invoice import Invoice
from .user import User

class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='sales', on_delete=models.CASCADE, null=True, blank=True)
    business = models.ForeignKey(Business, related_name='sales', on_delete=models.CASCADE)
    date = models.DateTimeField('Date', auto_now_add=True)
    total_amount = models.DecimalField('Total Amount', max_digits=10, decimal_places=2)
    items = models.ManyToManyField(InventoryItem, through='SaleItem')
    invoice = models.ForeignKey(Invoice, related_name='sales', on_delete=models.CASCADE, null=True, blank=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)