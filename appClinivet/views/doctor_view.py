from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.doctor import Doctor
from ..models.user import User
from ..serializers.doctor_serializer import DoctorSerializer
from ..serializers.user_serializer import UserSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_admin=False)

        doctor_serializer = self.get_serializer(data={"user": user.id, **request.data['doctor']})
        doctor_serializer.is_valid(raise_exception=True)
        doctor_serializer.save()

        token_data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        token_serializer = TokenObtainPairSerializer(data=token_data)
        token_serializer.is_valid(raise_exception=True)

        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)