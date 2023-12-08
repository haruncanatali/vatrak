from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductApiHandler.as_view(), name='product_handler'),
    path('<int:product_id>', views.ProductApiHandler.as_view(), name='product_detail_handler'),
    path('list', views.ProductListApiHandler.as_view(), name="product_list_handler"),
]
