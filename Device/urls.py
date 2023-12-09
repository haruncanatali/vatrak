from django.urls import path
from Device.views import DeviceApiHandler, DeviceListApiHandler

urlpatterns = [
    path('', DeviceApiHandler.as_view(), name='device_handler'),
    path('<int:device_id>', DeviceApiHandler.as_view(), name='device_detail_handler'),
    path('list', DeviceListApiHandler.as_view(), name='device_list_handler'),
]
