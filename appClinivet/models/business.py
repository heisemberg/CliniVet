from django.db import models

class Business(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Business Name', max_length=255)
    address = models.CharField('Address', max_length=255)
    phone_number = models.CharField('Phone Number', max_length=15)
    email = models.EmailField('Email', max_length=100, unique=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    def __str__(self):
        return self.name