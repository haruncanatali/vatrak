"""
URL configuration for vatrak project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from Product.urls import urlpatterns as product_urls
from Category.urls import urlpatterns as category_urls
from Order.urls import urlpatterns as order_urls
from Cart.urls import urlpatterns as cart_urls
from Device.urls import urlpatterns as device_urls
from Report.urls import urlpatterns as report_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include(product_urls)),
    path('category/', include(category_urls)),
    path('order/', include(order_urls)),
    path('cart/', include(cart_urls)),
    path('device/', include(device_urls)),
    path('report/', include(report_urls))
]
