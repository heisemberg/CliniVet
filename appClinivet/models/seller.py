from django.db import models
from .user import User

class Seller(models.Model):
    user = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)
    phone_number = models.CharField('Phone Number', max_length=15)
    address = models.CharField('Address', max_length=255)
