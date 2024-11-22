from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.user import User
from ..serializers.user_serializer import UserSerializer

class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.is_active = True
        user.save()
        
        token_data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        token_serializer = TokenObtainPairSerializer(data=token_data)
        token_serializer.is_valid(raise_exception=True)

        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)