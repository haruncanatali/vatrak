from rest_framework import serializers
from Device.models import Devices
from Cart.serializers import CartSerializer


class DeviceSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()

    def get_cart(self, obj):
        carts = obj.carts.all().first()
        serialized_cart = CartSerializer(carts, many=False).data
        return serialized_cart

    class Meta:
        model = Devices
        fields = ('id', 'name', 'battery', 'locked', 'last_locked_date', 'last_unlocked_date', 'cart')


class DevicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('name', 'battery', 'locked', 'last_locked_date', 'last_unlocked_date')


class DevicePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('id', 'name', 'battery', 'locked', 'last_locked_date', 'last_unlocked_date')
