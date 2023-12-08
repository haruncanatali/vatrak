from django.http import JsonResponse
from django.views import View
from django.db.models import Prefetch
from Cart.models import Carts
from Cart.serializers import CartSerializer, CartPostSerializer, CartPutSerializer
from Device.serializers import DeviceSerializer
from Device.models import Devices
from Report.models import Reports
from Order.models import Orders
import json


class CartApiHandler(View):
    def get(self, request, cart_id):
        response = {'success': False}

        cart = Carts.objects.prefetch_related('orders').filter(id=cart_id).first()

        if not cart:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False, status=400)

        cart_serialize = CartSerializer(cart, many=False)

        response['cart'] = cart_serialize.data
        response['success'] = True

        return JsonResponse(response)

    def post(self, request):
        response = {}

        cart_data = json.loads(request.body)

        device = Devices.objects.filter(id=cart_data["device_id"]).first()

        if not device:
            response["message"] = "Device not found."
            return JsonResponse(response, safe=False)

        cart_serializer = CartPostSerializer(data=cart_data)

        if not cart_serializer.is_valid():
            response['success'] = "False"
            response['message'] = "Request is not valid."
            return JsonResponse(response, safe=False)

        Carts.objects.create(total=cart_data["total"], device=device, payment_status=cart_data["payment_status"])

        response['success'] = True
        return JsonResponse(response, safe=False)

    def put(self, request):
        response = {}

        cart_data = json.loads(request.body)

        device = Devices.objects.filter(id=cart_data["device_id"]).first()

        if not device:
            response["success"] = False
            response["message"] = "Device not found."
            return JsonResponse(response, safe=False, status=400)

        cart = Carts.objects.filter(id=cart_data["id"]).first()

        if not cart:
            response["success"] = False
            response["message"] = "Cart not found."
            return JsonResponse(response, safe=False, status=400)

        cart_serializer = CartPutSerializer(data=cart_data)

        if not cart_serializer.is_valid():
            response['success'] = "False"
            response['message'] = "Request is not valid."
            return JsonResponse(response, safe=False)

        cart.total = cart_data["total"]
        cart.device = device
        cart.payment_status = cart_data["payment_status"]

        cart.save()

        response['success'] = True
        return JsonResponse(response, safe=False)

    def delete(self, request, cart_id):
        response = {}
        cart = Carts.objects.filter(id=cart_id).first()

        if not cart:
            response["success"] = False
            response["message"] = "Entity was not found."
            return JsonResponse(response, safe=False, status=400)

        orders = Orders.objects.filter(cart_id=cart_id).all()

        if orders:
            response["success"] = False
            response["message"] = "Please check if there are products in the cart."
            return JsonResponse(response, safe=False, status=400)

        cart.delete()

        response["success"] = True
        return JsonResponse(response, safe=False)


class PayingBillsApiHandler(View):
    def put(self, request, cart_id):
        response = {}

        cart = Carts.objects.prefetch_related(
            Prefetch('orders', queryset=Orders.objects.select_related('product'))
        ).filter(id=cart_id).first()

        if not cart:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False, status=400)

        cart_serialize = CartSerializer(cart, many=False).data

        device = Devices.objects.filter(id=cart_serialize["device_id"]).first()

        if not device:
            response['success'] = False
            response['message'] = 'Device was not found.'
            return JsonResponse(response, safe=False, status=400)

        device_serialize = DeviceSerializer(device, many=False).data
        orders = cart_serialize["orders"]

        if not orders:
            response["success"] = False
            response["message"] = "Orders in the cart not be found."
            return JsonResponse(response, safe=False, status=400)

        for order in orders:
            order = dict(order)
            report = Reports.objects.create(
                device_id=device_serialize["id"],
                device_name=device_serialize["name"],
                product_id=order["product"]["id"],
                product_name=order["product"]["name"],
                product_price=order["product"]["price"],
                amount=order["amount"],
                price=order["price"],
                order_date=order["date"]
            )
            report.save()

        Orders.objects.filter(cart_id=cart_id).delete()

        cart.total = 0.0
        cart.payment_status = True

        cart.save()

        response["success"] = True
        return JsonResponse(response, safe=False)
