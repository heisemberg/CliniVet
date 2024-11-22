from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.pet import Pet
from ..serializers.pet_serializer import PetSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # Only the owner can edit or delete
        return obj.owner == request.user.client

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pet.objects.all()
        return Pet.objects.filter(owner=user.client)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(owner=self.request.user.client)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.owner != self.request.user.client:
            raise PermissionDenied("You do not have permission to edit this pet.")
        serializer.save()

    from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.pet import Pet
from ..serializers.pet_serializer import PetSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # Only the owner can edit or delete
        return obj.owner == request.user.client

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pet.objects.all()
        return Pet.objects.filter(owner=user.client)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(owner=self.request.user.client)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.owner != self.request.user.client:
            raise PermissionDenied("You do not have permission to edit this pet.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.owner != self.request.user.client:
            raise PermissionDenied("You do not have permission to delete this pet.")
        instance.delete()