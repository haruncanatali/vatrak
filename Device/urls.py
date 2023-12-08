from django.urls import path
from Device.views import DeviceApiHandler

urlpatterns = [
    path('', DeviceApiHandler.as_view(), name='device_handler'),
]