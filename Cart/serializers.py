from rest_framework import serializers
from Cart.models import Carts
from Order.serializers import OrdersForCartSerializer, OrdersForReportSerializer


class CartSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    def get_orders(self, obj):
        orders = obj.orders.all()
        serialized_orders = OrdersForCartSerializer(orders, many=True).data
        return serialized_orders

    class Meta:
        model = Carts
        fields = ('id', 'total', 'device_id', 'orders')


class CartForReportSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    def get_orders(self, obj):
        orders = obj.orders.all()
        serialized_orders = OrdersForReportSerializer(orders, many=True).data
        return serialized_orders

    class Meta:
        model = Carts
        fields = ('id', 'total', 'device_id', 'orders')


class CartPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('total', 'device_id')


class CartPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('id', 'total', 'device_id')
