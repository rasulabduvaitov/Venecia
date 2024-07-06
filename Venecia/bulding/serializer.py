from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Flour, Block, House

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    houses = HouseSerializer(many=True, read_only=True)

    class Meta:
        model = Block
        fields = ['id', 'name', 'flour', 'available', 'sold', 'not_fully_paid', 'reserved', 'houses']


class BlockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['name', 'flour']


class FlourSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Flour
        fields = ['id', 'number', 'available', 'sold', 'not_fully_paid', 'reserved', 'blocks']


class FlourShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flour
        fields = ['id', 'number', 'available', 'sold', 'not_fully_paid', 'reserved']


class FlourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flour
        fields = ['number']
