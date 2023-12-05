from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductApiHandler.as_view(), name='product_handler'),
    path('<int:product_id>/', views.ProductApiHandler.as_view(), name='product_handler'),
]