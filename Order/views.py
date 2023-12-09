from django.http.response import JsonResponse
from django.views import View
import json
from Product.models import Products
from Cart.models import Carts
from Order.models import Orders
from Order.serializers import OrderSerializer, OrderPostSerializer, OrderPutSerializer
from Order.utils import get_order_count_in_cart
from Report.models import BatteryReports


class OrderApiHandler(View):
    def get(self, request, order_id):
        response = {'order': {}, 'success': False}

        order = Orders.objects.filter(id=order_id).first()

        if not order:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False)

        order_serialize = OrderSerializer(order, many=False)

        response['success'] = True
        response['order'] = order_serialize.data

        return JsonResponse(response, safe=False)

    def post(self, request):
        response = {'success': False}

        order_data = json.loads(request.body)

        order_serializer = OrderPostSerializer(data=order_data)
        if not order_serializer.is_valid():
            response['message'] = 'Parameters not valid.'
            return JsonResponse(response, safe=False, status=400)

        product = Products.objects.filter(id=order_data["product_id"]).first()

        if not product:
            response['message'] = 'Product not found.'
            return JsonResponse(response, safe=False, status=400)

        cart = Carts.objects.filter(id=order_data["cart_id"]).first()

        if not cart:
            response['message'] = 'Cart not found.'
            return JsonResponse(response, safe=False, status=400)

        order_count = get_order_count_in_cart(order_data["cart_id"])

        price = (int(order_data["amount"])) * (product.price)

        cart.total = cart.total + price

        cart.save()

        Orders.objects.create(date=order_data["date"], product=product, cart=cart, amount=int(order_data["amount"]), price=price)

        if order_count == 0:
            battery_report = BatteryReports.objects.create(
                entry=True,
                device_id=cart.device.id,
                battery=cart.device.battery
            )
            battery_report.save()

        response['success'] = True
        return JsonResponse(response, safe=False)

    def put(self, request):
        response = {'success': False}

        order_data = json.loads(request.body)
        order = Orders.objects.filter(id=order_data['id']).first()

        if not order:
            response["success"] = False
            response["message"] = "Entity was not found."

        order_serializer = OrderPutSerializer(order, data=order_data)
        if not order_serializer.is_valid():
            response["message"] = "Request not valid."
            return JsonResponse(response, safe=False)

        cart = Carts.objects.filter(id=order_data["cart_id"]).first()

        if not cart:
            response['message'] = 'Cart not found.'
            return JsonResponse(response, safe=False)

        product = Products.objects.filter(id=order_data["product_id"]).first()

        if not product:
            response['message'] = 'Product not found.'
            return JsonResponse(response, safe=False)

        price = (int(order_data["amount"])) * (product.price)

        l_price = (cart.total - order.price) + price
        cart.total = l_price
        cart.save()

        order.price = price
        order.date = order_data["date"]
        order.product = product
        order.cart = cart
        order.amount = order_data["amount"]

        order.save()

        response["success"] = True
        return JsonResponse(response, safe=False)

    def delete(self, request, order_id):
        response = {}
        order = Orders.objects.get(id=order_id)

        if not order:
            response["message"] = "Order was not found."
            response["success"] = False
            return JsonResponse(response, safe=False, status=400)

        cart = Carts.objects.filter(id=order.cart.id).first()
        cart.total = cart.total - order.price
        cart.save()

        order.delete()
        return JsonResponse(True, safe=False)


class OrderListApiHandler(View):
    def get(self, request):
        response = {'orders': [{}], 'success': False}

        orders = Orders.objects.all()

        if not orders:
            response['success'] = False
            response['message'] = 'Entities was not found.'
            return JsonResponse(response, safe=False)

        orders_serialize = OrderSerializer(orders, many=True)

        response['success'] = True
        response['orders'] = orders_serialize.data

        return JsonResponse(response)
