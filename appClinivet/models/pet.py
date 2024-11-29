from django.db import models
from .client import Client
from .business import Business

class Pet(models.Model):
    name = models.CharField('Name', max_length=100)
    species = models.CharField('Species', max_length=100)
    breed = models.CharField('Breed', max_length=100)
    age = models.IntegerField('Age')
    owner = models.ForeignKey(Client, related_name='pets', on_delete=models.CASCADE)
    business = models.ForeignKey(Business, related_name='pets', on_delete=models.CASCADE)