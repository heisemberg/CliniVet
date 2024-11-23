from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.pet import Pet
from ..serializers.pet_serializer import PetSerializer
from ..permissions import IsOwnerOrAdmin

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
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this pet.")
        instance.delete()