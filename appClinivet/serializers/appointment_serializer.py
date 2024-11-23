from rest_framework import serializers
from ..models.appointment import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'availability', 'reason', 'invoice']