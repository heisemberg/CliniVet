from rest_framework import status, viewsets, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.user import User
from ..serializers.user_serializer import UserSerializer


class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


    def create(self, request, *args, **kwargs):
        # Imprimir los datos proporcionados en la solicitud
        # print(f"Datos proporcionados: {request.data}")

        serializer = self.get_serializer(data=request.data)
        
        # Verificar si los datos son válidos
        if not serializer.is_valid():
            # print(f"Errores de validación: {serializer.errors}")
            serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        user.is_active = True
        user.save()

        # print(f"Usuario creado: {user.username}, Activo: {user.is_active}")

        # Verificar que la contraseña se haya configurado correctamente
        # print(f"Contraseña del usuario (hash): {user.password}")

        token_data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        # print(f"Datos del token: {token_data}")

        token_serializer = TokenObtainPairSerializer(data=token_data)
        
        if not token_serializer.is_valid():
            # print(f"Error en la generación del token: {token_serializer.errors}")
            raise serializers.ValidationError("Error en la generación del token")

        # print(f"Token generado para el usuario: {user.username}")

        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)