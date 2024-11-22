from django.db import models
from .user import User

class Client(models.Model):
    user =models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    address = models.CharField('Address', max_length=255)
    phone_number = models.CharField('Phone Number', max_length=15)
    last_change_date = models.DateTimeField()
    is_active = models.BooleanField('Is Active', default=True)