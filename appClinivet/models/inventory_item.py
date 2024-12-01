from django.db import models
from .business import Business

class InventoryItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_code = models.CharField('Product Code', max_length=100, unique=True)
    name = models.CharField('Name', max_length=255)
    category = models.CharField('Category', max_length=255)
    description = models.TextField('Description', blank=True, null=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity')
    business = models.ForeignKey(Business, related_name='inventory_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name