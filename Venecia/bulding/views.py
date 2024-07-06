from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    UserSerializer, AdminUserSerializer, FlourSerializer,
    FlourCreateSerializer, BlockSerializer, BlockCreateSerializer, HouseSerializer, FlourShortSerializer
)
from .models import Flour, Block, House
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
            )
        return Response({'error': 'Invalid Credentials'}, status=400)


class CreateUserView(CreateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = (DjangoModelPermissions,)


class FlourViewSet(viewsets.ModelViewSet):
    queryset = Flour.objects.all()
    serializer_class = FlourCreateSerializer
    permission_classes = [DjangoModelPermissions]
    lookup_field = 'number'

    def create(self, request, *args, **kwargs):
        serializer = FlourCreateSerializer(data=request.data)
        if serializer.is_valid():
            flour = serializer.save()
            self.update_status_counts(flour)
            response_serializer = FlourSerializer(flour)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_status_counts(instance)
        serializer = FlourSerializer(instance)
        return Response(serializer.data)

    def update_status_counts(self, flour):
        blocks = Block.objects.filter(flour=flour).all()
        flour.sold = sum(block.houses.filter(status=House.Status.SOLD).count() for block in blocks)
        flour.reserved = sum(block.houses.filter(status=House.Status.RESERVED).count() for block in blocks)
        flour.not_fully_paid = sum(block.houses.filter(status=House.Status.NOT_FULLY_PAID).count() for block in blocks)
        flour.available = sum(block.houses.filter(status=House.Status.AVAILABLE).count() for block in blocks)
        flour.save()

    @action(methods=['GET'], detail=True)
    def get_statistics(self, request, number=None):
        instance = self.get_object()
        self.update_status_counts(instance)
        serializer = FlourShortSerializer(instance)
        return Response(serializer.data)


class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockCreateSerializer
    permission_classes = (DjangoModelPermissions,)

    def create(self, request, *args, **kwargs):
        serializer = BlockCreateSerializer(data=request.data)
        if serializer.is_valid():
            block = serializer.save()
            self.update_status_counts(block)
            response_serializer = BlockSerializer(block)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_status_counts(instance)
        serializer = BlockSerializer(instance)
        return Response(serializer.data)

    def update_status_counts(self, block):
        houses = block.houses.all()
        block.sold = houses.filter(status=House.Status.SOLD).count()
        block.reserved = houses.filter(status=House.Status.RESERVED).count()
        block.not_fully_paid = houses.filter(status=House.Status.NOT_FULLY_PAID).count()
        block.available = houses.filter(status=House.Status.AVAILABLE).count()
        block.save()


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = (DjangoModelPermissions,)
