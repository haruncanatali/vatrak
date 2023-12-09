from rest_framework import serializers
from Category.models import Categories
from Product.serializers import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = obj.products.all()
        serialized_products = ProductSerializer(products, many=True).data
        return serialized_products

    class Meta:
        model = Categories
        fields = ('id', 'name', 'products')


class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name',)


class CategoryPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')
