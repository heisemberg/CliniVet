from django.db import models
from .user import User

class Admin(models.Model):
    user = models.OneToOneField(User, related_name='admin', on_delete=models.CASCADE)
    phone_number = models.CharField('Phone Number', max_length=15)
    address = models.CharField('Address', max_length=255)