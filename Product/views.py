from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views import View
import json


from Product.models import Products
from Product.serializers import ProductSerializer


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
        product = Products.objects.get(id=product_id)
        product.delete()
        return JsonResponse(True, safe=False)