from django.db import models
from .client import Client

class Pet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Name', max_length=50)
    species = models.CharField('Species', max_length=50)
    breed = models.CharField('Breed', max_length=50)
    age = models.IntegerField('Age')
    owner = models.ForeignKey(Client, related_name='pets', on_delete=models.CASCADE)