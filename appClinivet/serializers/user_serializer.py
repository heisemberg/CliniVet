from rest_framework import serializers
from ..models.user import User
from ..models.admin import Admin
from ..models.doctor import Doctor
from ..models.client import Client
from .admin_serializer import AdminSerializer
from .doctor_serializer import DoctorSerializer
from .client_serializer import ClientSerializer

class UserSerializer(serializers.ModelSerializer):
    admin = AdminSerializer(required=False)
    doctor = DoctorSerializer(required=False)
    client = ClientSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'is_admin', 'admin', 'doctor', 'client']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        client_data = validated_data.pop('client', None)
        
        user = User.objects.create(**validated_data)
        
        if admin_data:
            Admin.objects.create(user=user, **admin_data)
        elif doctor_data:
            Doctor.objects.create(user=user, **doctor_data)
        elif client_data:
            Client.objects.create(user=user, **client_data)
        
        return user

    def update(self, instance, validated_data):
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        client_data = validated_data.pop('client', None)
        
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        if admin_data:
            Admin.objects.update_or_create(user=instance, defaults=admin_data)
        elif doctor_data:
            Doctor.objects.update_or_create(user=instance, defaults=doctor_data)
        elif client_data:
            Client.objects.update_or_create(user=instance, defaults=client_data)
        
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'admin'):
            representation['admin'] = AdminSerializer(instance.admin).data
        if hasattr(instance, 'doctor'):
            representation['doctor'] = DoctorSerializer(instance.doctor).data
        if hasattr(instance, 'client'):
            representation['client'] = ClientSerializer(instance.client).data
        return representation