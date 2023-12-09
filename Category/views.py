from django.http import JsonResponse
from django.views import View
from Category.models import Categories
from Category.serializers import CategorySerializer, CategoryPostSerializer, CategoryPutSerializer
import json


class CategoryApiHandler(View):
    def get(self, request, category_id):
        response = {}
        category = Categories.objects.filter(id=category_id).first()

        if not category:
            response["success"] = False
            response["message"] = "Category was not found."
            return JsonResponse(response, safe=False, status=400)

        category_serializer = CategorySerializer(category, many=False)

        response["success"] = True
        response["category"] = category_serializer.data
        return JsonResponse(response, safe=False)

    def post(self, request):
        response = {}
        category_data = json.loads(request.body)

        category_serializer = CategoryPostSerializer(data=category_data)

        if not category_serializer.is_valid():
            response["success"] = False
            response["message"] = "Request is not valid."
            return JsonResponse(response, safe=False, status=400)

        category_serializer.save()

        response["success"] = True
        return JsonResponse(response, safe=False)

    def put(self, request):
        response = {}
        category_data = json.loads(request.body)

        category = Categories.objects.filter(id=category_data["id"]).first()

        if not category:
            response["success"] = False
            response["message"] = "Category was not found."
            return JsonResponse(response, safe=False, status=400)

        category_serializer = CategoryPutSerializer(category, data=category_data)

        if category and category_serializer.is_valid():
            category_serializer.save()
            response["success"] = True
            return JsonResponse(response, safe=False)
        else:
            response["success"] = False
            response["message"] = "Request is not valid."
            return JsonResponse(response, safe=False, status=400)

    def delete(self, request, category_id):
        response = {}
        category = Categories.objects.filter(id=category_id).first()

        if not category:
            response["success"] = False
            response["message"] = "Category was not found."
            return JsonResponse(response, safe=False, status=400)

        category_serializer = CategorySerializer(category).data

        if category_serializer["products"] and len(category_serializer["products"]) > 0:
            response["success"] = False
            response["message"] = "There are products in this category. Replace the products first."
            return JsonResponse(response, safe=False, status=400)

        category.delete()

        response["success"] = True
        return JsonResponse(response, safe=False)


class CategoryListApiHandler(View):
    def get(self, request):
        response = {}
        categories = Categories.objects.prefetch_related('products').all()

        if not categories:
            response["success"] = False
            response["message"] = "Entities not found."
            return JsonResponse(response, safe=False, status=400)

        categories_serializer = CategorySerializer(categories, many=True)

        response["success"] = True
        response["categories"] = categories_serializer.data

        return JsonResponse(response, safe=False)
