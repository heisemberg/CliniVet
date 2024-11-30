from rest_framework import status, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.user import User
from ..serializers.user_serializer import UserSerializer

class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []  # Permitir acceso sin autenticación para registrar un usuario
        return [IsAuthenticated()]  # Requerir autenticación para otras acciones

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.filter(business=user.business)
        return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # Verificar si los datos son válidos
        if not serializer.is_valid():
            serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        # Activar el usuario
        user.is_active = True
        user.save()

        # Preparar la respuesta
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)