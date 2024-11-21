from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.admin import Admin
from ..models.user import User
from ..serializers.admin_serializer import AdminSerializer
from ..serializers.user_serializer import UserSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_admin=True)

        admin_serializer = self.get_serializer(data={"user": user.id})
        admin_serializer.is_valid(raise_exception=True)
        admin_serializer.save()

        token_data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        token_serializer = TokenObtainPairSerializer(data=token_data)
        token_serializer.is_valid(raise_exception=True)

        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)