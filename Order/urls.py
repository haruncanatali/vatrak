from django.urls import path
from .views import OrderApiHandler, OrderListApiHandler

urlpatterns = [
    path('', OrderApiHandler.as_view(), name='order_handler'),
    path('<int:order_id>', OrderApiHandler.as_view(), name='order_detail_handler'),
    path('list', OrderListApiHandler.as_view(), name='order_list_handler')
]
