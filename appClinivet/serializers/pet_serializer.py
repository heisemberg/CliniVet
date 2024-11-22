from rest_framework import serializers
from ..models.pet import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'age', 'owner']
