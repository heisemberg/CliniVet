from django.db import models
from .client import Client
from .inventory_item import InventoryItem
from .business import Business
from .user import User
from .appointment import Appointment

class Invoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='invoices', on_delete=models.CASCADE)
    business = models.ForeignKey(Business, related_name='invoices', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='invoices', on_delete=models.CASCADE)
    date = models.DateTimeField('Date', auto_now_add=True)
    total_amount = models.DecimalField('Total Amount', max_digits=10, decimal_places=2)
    service_cost = models.DecimalField('Service Cost', max_digits=10, decimal_places=2, default=0.00)
    exam_cost = models.DecimalField('Exam Cost', max_digits=10, decimal_places=2, default=0.00)
    items = models.ManyToManyField(InventoryItem, through='InvoiceItem')
    appointment = models.OneToOneField(Appointment, related_name='invoice', on_delete=models.CASCADE, null=True, blank=True)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)