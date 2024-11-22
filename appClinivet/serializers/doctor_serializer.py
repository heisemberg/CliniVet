from rest_framework import serializers
from ..models.doctor import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['license_number', 'specialty','phone_number', 'address' , 'last_change_date', 'is_active']

