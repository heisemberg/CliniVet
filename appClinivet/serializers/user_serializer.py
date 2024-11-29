from rest_framework import serializers
from ..models.user import User
from ..models.client import Client
from ..models.admin import Admin
from ..models.doctor import Doctor
from ..models.seller import Seller
from ..models.business import Business
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
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'business', 'client', 'admin', 'doctor', 'seller']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        client_data = validated_data.pop('client', None)
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        seller_data = validated_data.pop('seller', None)
        business = validated_data.pop('business', None)
        
        if admin_data:
            userInstance = User.objects.create_superuser(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                business=business
            )
            Admin.objects.create(user=userInstance, **admin_data)
        else:
            userInstance = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                business=business
            )
            
        if client_data:
            Client.objects.create(user=userInstance, business=business, **client_data)
        if doctor_data:
            Doctor.objects.create(user=userInstance, business=business, **doctor_data)
        if seller_data:
            Seller.objects.create(user=userInstance, business=business, **seller_data)
        
        return userInstance

    def update(self, instance, validated_data):
        client_data = validated_data.pop('client', None)
        admin_data = validated_data.pop('admin', None)
        doctor_data = validated_data.pop('doctor', None)
        seller_data = validated_data.pop('seller', None)
        business = validated_data.pop('business', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if client_data:
            if hasattr(instance, 'client'):
                for attr, value in client_data.items():
                    setattr(instance.client, attr, value)
                instance.client.save()
            else:
                Client.objects.create(user=instance, business=business, **client_data)
        
        if admin_data:
            if hasattr(instance, 'admin'):
                for attr, value in admin_data.items():
                    setattr(instance.admin, attr, value)
                instance.admin.save()
            else:
                Admin.objects.create(user=instance, business=business, **admin_data)
        
        if doctor_data:
            if hasattr(instance, 'doctor'):
                for attr, value in doctor_data.items():
                    setattr(instance.doctor, attr, value)
                instance.doctor.save()
            else:
                Doctor.objects.create(user=instance, business=business, **doctor_data)
        
        if seller_data:
            if hasattr(instance, 'seller'):
                for attr, value in seller_data.items():
                    setattr(instance.seller, attr, value)
                instance.seller.save()
            else:
                Seller.objects.create(user=instance, business=business, **seller_data)
        
        return instance

    def to_representation(self, instance):
        user = User.objects.get(id=instance.id)
        representation = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'business': user.business.id
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