from rest_framework import serializers
from ..models.client import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['phone_number', 'address',  'last_change_date', 'is_active']

    