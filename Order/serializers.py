from rest_framework import serializers
from Order.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return obj.product.serialize()

    class Meta:
        model = Orders
        fields = ('id', 'date', 'amount', 'price', 'cart_id', 'product')


class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('date', 'amount', 'product_id', 'cart_id')


class OrderPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'date', 'amount', 'product_id', 'cart_id')


class OrdersForCartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return obj.product.serialize()

    class Meta:
        model = Orders
        fields = ('id', 'date', 'amount', 'price', 'product')
