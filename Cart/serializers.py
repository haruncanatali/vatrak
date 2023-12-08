from rest_framework import serializers
from Cart.models import Carts
from Order.serializers import OrdersForCartSerializer


class CartSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    def get_orders(self, obj):
        orders = obj.orders.all()
        serialized_orders = OrdersForCartSerializer(orders, many=True).data
        return serialized_orders

    class Meta:
        model = Carts
        fields = ('id', 'total', 'payment_status', 'device_id', 'orders')


class CartPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('total', 'payment_status', 'device_id')


class CartPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('id', 'total', 'payment_status', 'device_id')
