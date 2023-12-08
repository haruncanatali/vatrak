from django.http.response import JsonResponse
from django.views import View
import json

from Product.models import Products
from Product.serializers import ProductSerializer
from Cart.models import Carts


class ProductApiHandler(View):
    def get(self, request, product_id):
        response = {'product': {}, 'success': False}
        product = Products.objects.filter(id=product_id).first()
        products_serializer = ProductSerializer(product, many=False)

        if product:
            response['product'] = products_serializer.data
            response['success'] = True
            return JsonResponse(response, safe=False)

        response['message'] = 'Entity not found.'
        return JsonResponse(response, safe=False)

    def post(self, request):
        product_data = json.loads(request.body)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(True, safe=False)
        return JsonResponse(False, safe=False)

    def put(self, request):
        response = {'success': False}
        product_data = json.loads(request.body)
        product = Products.objects.filter(id=product_data['id']).first()
        product_serializer = ProductSerializer(product, data=product_data)
        if product_serializer.is_valid() and product:
            product_serializer.save()
            response['success'] = True
            return JsonResponse(True, safe=False)

        response['message'] = 'Entity not found.'
        return JsonResponse(response, safe=False)

    def delete(self, request, product_id):
        response = {"success": False}
        product = Products.objects.get(id=product_id)

        carts = Carts.objects.filter(product_id=product_id).all()

        if not carts:
            product.delete()
            response["success"] = True
            response["message"] = "Entity deleted."
            return JsonResponse(response, safe=False)

        response["message"] = "The entity could not be deleted. Please check whether the product you want to delete is in active carts."
        return JsonResponse(True, safe=False)


class ProductListApiHandler(View):
    def get(self, response):
        response = {}
        products = Products.objects.all()
        products_serializer = ProductSerializer(products, many=True)

        if products:
            response['products'] = products_serializer.data
            response['success'] = True
            return JsonResponse(response, safe=False)

        response['message'] = 'Entities not found.'
        response["success"] = False
        return JsonResponse(response, safe=False)
