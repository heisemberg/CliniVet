from django.db import models
from .user import User
from .business import Business

class Seller(models.Model):
    user = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)
    business = models.ForeignKey(Business, related_name='sellers', on_delete=models.CASCADE)
    phone_number = models.CharField('Phone Number', max_length=15)
    address = models.CharField('Address', max_length=255)