from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.user import User
from ..serializers.user_serializer import UserSerializer

class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # Permitir acceso sin autenticación para registrar un usuario

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