from rest_framework import serializers
from ..models.availability import Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_occupied']