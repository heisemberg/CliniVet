from rest_framework import serializers
from ..models.user import User
from ..models.client import Client
from ..models.admin import Admin
from ..models.doctor import Doctor
from ..models.seller import Seller
from ..serializers.client_serializer import ClientSerializer
from ..serializers.admin_serializer import AdminSerializer
from ..serializers.doctor_serializer import DoctorSerializer
from ..serializers.seller_serializer import SellerSerializer

class UserSerializer(serializers.ModelSerializer):
    client = ClientSerializer(required=False)
    admin = AdminSerializer(required=False)
    doctor = DoctorSerializer(required=False)
    seller = SellerSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'client', 'admin', 'doctor', 'seller']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        client_data = validated_data.pop('client', None)
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        seller_data = validated_data.pop('seller', None)
        
        if admin_data:
            userInstance = User.objects.create_superuser(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password']
            )
            Admin.objects.create(user=userInstance, **admin_data)
        else:
            userInstance = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password']
            )
            
            if client_data:
                Client.objects.create(user=userInstance, **client_data)
            if doctor_data:
                Doctor.objects.create(user=userInstance, **doctor_data)
            if seller_data:
                Seller.objects.create(user=userInstance, **seller_data)
        
        return userInstance

    def update(self, instance, validated_data):
        client_data = validated_data.pop('client', None)
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        seller_data = validated_data.pop('seller', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if client_data:
            client = instance.client
            for attr, value in client_data.items():
                setattr(client, attr, value)
            client.save()
        if admin_data:
            admin = instance.admin
            for attr, value in admin_data.items():
                setattr(admin, attr, value)
            admin.save()
        if doctor_data:
            doctor = instance.doctor
            for attr, value in doctor_data.items():
                setattr(doctor, attr, value)
            doctor.save()
        if seller_data:
            seller = instance.seller
            for attr, value in seller_data.items():
                setattr(seller, attr, value)
            seller.save()
        
        return instance

    def to_representation(self, instance):
        user = User.objects.get(id=instance.id)
        representation = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        if hasattr(user, 'client'):
            representation['client'] = ClientSerializer(user.client).data
        if hasattr(user, 'admin'):
            representation['admin'] = AdminSerializer(user.admin).data
        if hasattr(user, 'doctor'):
            representation['doctor'] = DoctorSerializer(user.doctor).data
        if hasattr(user, 'seller'):
            representation['seller'] = SellerSerializer(user.seller).data
        return representation