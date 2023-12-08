from django.shortcuts import render
from django.views import View
from Device.models import Devices

class DeviceApiHandler(View):

    def get(self, request, device_id):
        response = {'device': {}, 'success': False}

        device = Devices.objects.filter(id=device_id).all().first()

        if not device:
            response['success'] = False
            response['message'] = 'Entity was not found.'
            return JsonResponse(response, safe=False)

        cart_serialize = CartSerializer(cart, many=False)

        response['success'] = True
        response['cart'] = cart_serialize.data

        return JsonResponse(response)
