from rest_framework import serializers
from Product.models import Products
from Category.models import Categories


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer()

    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'photo', 'category')


class ProductByCategoryReportSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Products
        fields = ('name', 'price', 'category')


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'price', 'photo', 'category')


class ProductPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'photo', 'category')
