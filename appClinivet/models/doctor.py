from django.db import models
from .user import User

class Doctor(models.Model):
    user =models.OneToOneField(User, related_name='doctor', on_delete=models.CASCADE)
    license_number = models.CharField('License Number', max_length=50, unique=True)
    specialty = models.CharField('Specialty', max_length=100)
    phone_number = models.CharField('Phone Number', max_length=15)
    address = models.CharField('Address', max_length=255)