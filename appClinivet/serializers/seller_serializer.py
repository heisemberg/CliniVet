from rest_framework import serializers
from ..models.seller import Seller

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['phone_number', 'address']