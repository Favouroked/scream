import threading

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from users.utils import enrich_with_holiday_data, get_client_ip


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        ip = get_client_ip(request)
        th = threading.Thread(target=enrich_with_holiday_data, args=(data['email'], ip))
        th.start()

        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
