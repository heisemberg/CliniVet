from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.pet import Pet
from ..serializers.pet_serializer import PetSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]