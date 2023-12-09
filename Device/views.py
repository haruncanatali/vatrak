from django.http import JsonResponse
from django.views import View
from django.db.models import Prefetch
from Device.models import Devices
from Cart.models import Carts
from Device.serializers import DeviceSerializer, DevicePostSerializer, DevicePutSerializer
import json


class DeviceApiHandler(View):
    def get(self, request, device_id):
        response = {}

        device = Devices.objects.prefetch_related(Prefetch('carts', queryset=Carts.objects.prefetch_related('orders'))) \
            .filter(id=device_id).first()

        if not device:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False, status=400)

        device_serialize = DeviceSerializer(device, many=False)

        response['success'] = True
        response['device'] = device_serialize.data

        return JsonResponse(response, safe=False)

    def post(self, request):
        response = {}

        device_data = json.loads(request.body)

        device_serializer = DevicePostSerializer(data=device_data)

        if device_serializer.is_valid():
            device_serializer.save()
            response["success"] = True
            return JsonResponse(response, safe=False)

        response["success"] = False
        response["message"] = "Request is not valid."
        return JsonResponse(response, safe=False, status=400)

    def put(self, request):
        response = {}

        device_data = json.loads(request.body)

        device = Devices.objects.filter(id=device_data["id"]).all().first()

        if not device:
            response["success"] = False
            response["message"] = "Device is not found."
            return JsonResponse(response, safe=False, status=400)

        device_serializer = DevicePutSerializer(device, data=device_data)

        if device_serializer.is_valid():
            device_serializer.save()
            response["success"] = True
            return JsonResponse(response, safe=False)

        response["success"] = False
        response["message"] = "Request is not valid."
        return JsonResponse(response, safe=False, status=400)

    def delete(self, request, device_id):
        response = {}

        device = Devices.objects.prefetch_related(Prefetch('carts', queryset=Carts.objects.prefetch_related('orders'))) \
            .filter(id=device_id).first()

        if not device:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False, status=400)

        device_serialize = DeviceSerializer(device, many=False).data

        if device_serialize["carts"] and len(device_serialize["carts"]) > 0:
            response['success'] = False
            response['message'] = 'There is a cart registered to this device. First, delete the basket.'
            return JsonResponse(response, safe=False, status=400)

        device.delete()

        response["success"] = True
        return JsonResponse(response, safe=False)


class DeviceListApiHandler(View):
    def get(self, request):
        response = {}
        devices = Devices.objects.prefetch_related(Prefetch('carts', queryset=Carts.objects.prefetch_related('orders'))).all()
        if not devices:
            response['success'] = False
            response['message'] = 'Entities was not found.'
            return JsonResponse(response, safe=False, status=400)

        devices_serialize = DeviceSerializer(devices, many=True)
        response["success"] = True
        response["devices"] = devices_serialize.data

        return JsonResponse(response, safe=False)
