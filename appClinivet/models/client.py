from django.db import models
from .user import User

class Client(User):
    address = models.CharField('Address', max_length=255)
    phone_number = models.CharField('Phone Number', max_length=15)