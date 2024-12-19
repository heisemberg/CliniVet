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
            # Filtrar por el negocio del usuario autenticado
            return Pet.objects.filter(owner__business=user.business)
        return Pet.objects.filter(owner=user.client)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(owner=self.request.user.client)
        else:
            # Asignar el negocio del usuario autenticado al crear una mascota
            serializer.save(owner=self.request.user.client, business=self.request.user.business)

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.owner != self.request.user.client:
            raise PermissionDenied("You do not have permission to edit this pet.")
        serializer.save()