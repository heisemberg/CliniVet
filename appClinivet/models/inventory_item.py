from django.db import models

class InventoryItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Name', max_length=100)
    category = models.CharField('Category', max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity')