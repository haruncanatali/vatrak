from django.urls import path
from .views import CartApiHandler, PayingBillsApiHandler, CartListApiHandler

urlpatterns = [
    path('', CartApiHandler.as_view(), name='cart_handler'),
    path('<int:cart_id>', CartApiHandler.as_view(), name='cart_detail_handler'),
    path('payment/<int:cart_id>', PayingBillsApiHandler.as_view(), name='payment_handler'),
    path('list', CartListApiHandler.as_view(), name='cart_list_handler'),
]
