from rest_framework import serializers
from ..models.business import Business

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'created_at', 'updated_at']